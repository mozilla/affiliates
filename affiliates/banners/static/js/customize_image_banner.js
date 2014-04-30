/* global jQuery, rivets */
;(function($, rivets) {
    'use strict';

    // Base rivets config.
    rivets.configure({
        prefix: 'data-rv'
    });

    // Custom rivets binders/formatters.
    rivets.binders.disabled = function(el, value) {
        $(el).prop('disabled', !!value);
    };

    // Hacky workaround to get the disabled binder to pick up on changes when
    // the options available in a dropdown change. This forces a reset and
    // change event when a value the select depends on changes, which causes the
    // disabled binder to reevaluate and disable the right select boxes.
    rivets.binders.reset = function(el, value) {
        $(el).val('').change();
    };

    rivets.formatters.not = function(value) {
        return !value;
    };


    /**
     * Controller for the form that allows the user to choose which variation
     * of an ImageBanner that they want to use.
     */
    function VariationForm(elem) {
        this.dom = {};
        this.view = null;

        this.dom.form = $(elem);
        this.dom.locale = this.dom.form.find('select[name="locale"]');
        this.dom.size = this.dom.form.find('select[name="size"]');
        this.dom.color = this.dom.form.find('select[name="color"]');
        this.dom.preview = this.dom.form.find('img.preview');

        this.variations = this.dom.form.data('variations');
        this.selectedLocale = '';
        this.selectedSize = '';
        this.selectedColor = '';

        // Available locales never changes, so generate the list once.
        this.locales = this.findChoices('locale');
    }

    VariationForm.prototype = {
        /**
         * Bind controller to the form using rivets.
         */
        bind: function() {
            if (!this.view) {
                this.view = rivets.bind(this.dom.form, this);
            }
        },

        /**
         * Find possible choices from the set of variations for the given key,
         * optionally filtering by other keys.
         */
        findChoices: function(key, filters) {
            var choices = [];

            $.each(this.variations, function(pk, variation) {
                if (matchesFilters(variation, filters) &&
                    choices.indexOf(variation[key]) === -1) {
                    choices.push(variation[key]);
                }
            });

            return choices.sort();
        },

        /**
         * List of available sizes based on the currently selected locale.
         */
        sizes: function() {
            return this.findChoices('size', {locale: this.selectedLocale});
        },

        /**
         * List of available colors based on the currently selected locale and
         * size.
         */
        colors: function() {
            return this.findChoices('color', {
                locale: this.selectedLocale,
                size: this.selectedSize
            });
        },

        /**
         * PK of the variation that matches the currently selected locale, size,
         * and color.
         */
        variation: function() {
            var locale = this.selectedLocale;
            var size = this.selectedSize;
            var color = this.selectedColor;

            if (!locale || !size || !color) {
                return '';
            }

            var filters = {locale: locale, size: size, color: color};
            var match = '';
            $.each(this.variations, function(pk, variation) {
                if (matchesFilters(variation, filters)) {
                    match = pk;
                    return false;
                }
            });

            return match;
        },

        /**
         * Href to the currently selected variation's image.
         */
        previewSrc: function() {
            var pk = this.variation();
            if (pk !== '') {
                return this.variations[pk].image;
            } else {
                return '/static/img/banner-blank.png';
            }
        },

        /**
         * Href to the currently selected variation's update image. Only used
         * for upgrade banners.
         */
        upgradePreviewSrc: function() {
            var pk = this.variation();
            if (pk !== '') {
                return this.variations[pk].upgrade_image;
            } else {
                return '/static/img/banner-blank.png';
            }
        }
    };


    // Initialize widget if it's found on the current page.
    $(function() {
        var elem = document.getElementById('variation-choices');
        if (elem) {
            var form = new VariationForm(elem);
            form.bind();
        }
    });


    // Utility functions.
    function matchesFilters(obj, filters) {
        if (!filters) {
            return true;
        }

        var match = true;
        $.each(filters, function(key, value) {
            if (obj[key] !== value) {
                match = false;
                return false;
            }
        });

        return match;
    }
})(jQuery, rivets);
