/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';

    var open = false;
    var $window = $(window);
    var $document = $(document);
    var $body = $('body');
    var $navList = $('#nav-main-menu');
    var $navListSub = $('#nav-user-submenu');
    var $strings = $('#strings');
    var evtNamespace = 'moz-modal';

    // Add a class to use as a style hook when JavaScript is available
    $body.removeClass('no-js').addClass('js');

    // Trigger the .thin-mode class on <body> when the screen is thinner than
    // 760 pixels.
    $window.resize(function() {
        clearTimeout(this.resizeTimeoutId);
        this.resizeTimeoutId = setTimeout(doneResizing, 200);
    });

    function doneResizing() {
        if ($window.width() < 760) {
            $body.removeClass('wide-mode').addClass('thin-mode');
            $navList.attr('aria-hidden', 'true').hide();
        } else {
            $body.removeClass('thin-mode').addClass('wide-mode');
            $navList.removeAttr('aria-hidden').show();
        }
        $navListSub.removeAttr('style');
    }
    $(doneResizing);  // Call once when done loading the page to initialize.

    // Show/hide the main navigation in small viewports
    $document.on('click', '.thin-mode #nav-main .toggle', expandMainNav);
    $document.on('click', '.thin-mode #nav-main .toggle.open', collapseMainNav);
    $document.on('mouseleave', '.thin-mode #nav-main', collapseMainNav);

    function expandMainNav() {
        $navList.slideDown('fast').removeAttr('aria-hidden').attr('aria-expanded', 'true');
        $("#nav-main .toggle").addClass("open");
    }

    function collapseMainNav() {
        $navList.slideUp('fast').attr('aria-hidden', 'true').removeAttr('aria-expanded');
        $("#nav-main .toggle").removeClass("open");
    }

    // Show/hide the sub-navigation in wide viewports
    $document.on('mouseover', '.wide-mode #nav-main .user', expandSubNav);
    $document.on('click focus', '.wide-mode #nav-main .user > a', function(e) {
        e.preventDefault();
        expandSubNav();
    });
    $document.on('mouseleave', '.wide-mode #nav-main .user', collapseSubNav);

    function expandSubNav() {
        $navListSub.stop().slideDown('fast').removeAttr('aria-hidden').attr('aria-expanded', 'true');
        $("#nav-main .user").addClass("open");
    }

    function collapseSubNav() {
        $navListSub.stop().slideUp('fast').attr('aria-hidden', 'true').removeAttr('aria-expanded');
        $("#nav-main .user").removeClass("open");
    }

    // Lazy-load images that have data-src attributes.
    $(function() {
        $('img.lazy').show().unveil();
    });

    // Store common functions on affiliates global.
    var affiliates = {
        trans: function(stringId, data){
            var string = $strings.data(stringId);
            if (data) {
                for (var key in data) {
                    if (data.hasOwnProperty(key)) {
                        string = string.replace('%(' + key + ')s', data[key]);
                    }
                }
            }
            return string;
        },

        createModal: function(origin, content, bg_close) {
            // Clear existing modal, if necessary,
            if (open) {
                $('#modal').remove();
                $('.modalOrigin').removeClass('modalOrigin');
            }

            // If bg_close is false, we disable being able to close the modal
            // just by clicking the background.
            var modal_class = 'bg_close';
            if (!bg_close && bg_close !== undefined) {
                modal_class = '';
            }

            // Create new modal
            var $modal = $(
                '<div id="modal" tabindex="-1" role="dialog" aria-labelledby="' + origin.attr('id') + '" class="' + modal_class + '">' +
                '  <div class="inner">' +
                '    <button type="button" class="button secondary close">' +
                '      ' + affiliates.trans('close') +
                '    </button>' +
                '  </div>' +
                '</div>'
            );

            // Add the modal to the page.
            $('body').addClass('noscroll').append($modal);
            $('#modal .inner').prepend(content);
            $modal.fadeIn(200).focus();
            $(origin).addClass('modalOrigin');

            open = true;

            // Close modal on clicking close or background.
            $document.on('click', '#modal .close', affiliates.closeModal);
            $document.on('click', '#modal.bg_close', function(e){
                if (e.target === this) {
                    affiliates.closeModal();
                }
            });

            // Close on escape
            $document.on('keyup.' + evtNamespace, function(e) {
                if (open && e.keyCode === 27) { // esc
                    affiliates.closeModal();
                }
            });

            // prevent focusing out of modal while open
            $document.on('focus.' + evtNamespace, 'body', function(e) {
                // .contains must be called on the underlying HTML element, not the jQuery object
                if (open && !$modal[0].contains(e.target)) {
                    e.stopPropagation();
                    $modal.focus();
                }
            });

        },

        closeModal: function() {
            if (open) {
                $('#modal').fadeOut(200, function(){
                    $(this).remove();
                });
                $('body').removeClass('noscroll');
                $('.modalOrigin').focus().removeClass('modalOrigin');
                open = false;
                // unbind document listeners
                $document.off('.' + evtNamespace);
            }
        }

    };
    window.affiliates = affiliates;

    // Load some links in a full-page modal
    $('.has-modal').on('click', function(e) {
        e.preventDefault();
        var $origin = $(this);
        // Extract the target element's ID from the link's href.
        var elem = $origin.attr('href').replace( /.*?(#.*)/g, "$1" );
        var content = $(elem).html();
        affiliates.createModal($origin, content);
    });

    // Newsletter form.
    var $newsletterForm = $('#newsletter-form');
    var $newsletterFormMessage = $('#newsletter-message');

    function showFormMessage(msg) {
        $newsletterForm.find('ol').slideUp(function() {
            $newsletterFormMessage.find('p').text(msg);
            $newsletterFormMessage.slideDown();
        });
    }

    // Show extra fields
    $newsletterForm.find('#id_email').on('focus', function() {
        $newsletterForm.find('.form-extra').slideDown();
    });

    // Process form submission.
    $newsletterForm.on('submit', function(e) {
        e.preventDefault();

        var jqXHR = $.post($newsletterForm.attr('action'), $newsletterForm.serialize());
        jqXHR.done(function() {
            showFormMessage(affiliates.trans('subscribeThanks'));
        }).fail(function() {
            showFormMessage(affiliates.trans('subscribeError'));
        });
    });

})(jQuery);
