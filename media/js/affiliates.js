;(function($, MonthYearPicker) {
    'use strict';

    $.fn.affiliatesAccordion = function() {
        var lnkAction = $("h5 a", this);

        this.children().removeClass().addClass('collapsed');
        lnkAction.each(function(){
            $(this).click(function(e){
                e.preventDefault();
                var liElement = $(this).parents('li');
                var answerElement = $('.answer', liElement);
                if (liElement.hasClass('collapsed')) {
                    answerElement.slideDown('fast', function() {
                        liElement.removeClass().addClass('expanded');
                    });
                } else {
                    answerElement.slideUp('fast', function() {
                        liElement.removeClass().addClass('collapsed');
                    });
                }
            });
        });
    };

    $(function(event){
        // Init MonthYearPicker
        var monthYearPicker = new MonthYearPicker('.month-year-picker', {
            errorMsgSelector: '.statistics-warning'
        });
        monthYearPicker.onRefresh(function(data) {
            $('#your-downloads').text(data.user_total);
            $('#average-downloads').text(data.site_avg);
            if (data.fb_total) {
                $('#facebook-stats').show();
                $('#facebook-total-clicks').text(data.fb_total);
            }
        });

        // Enable placeholders in non-HTML5 browsers
        $('input[placeholder],textarea[placeholder]').placeholder();

        // Banner code textboxes should select all of their contents on focus
        $('textarea.embed-code').focus(function() {
            this.select();
        });

        // Activate accordion plugin.
        $(".js_accordion").each(function(index, elem){
            $(elem).affiliatesAccordion();
        });

        // Tooltips can't be clicked.
        $(".show_tooltip").click(function(e){
            e.preventDefault();
        });

        // Show and hide the target on hover.
        $(".show_tooltip").hover(
            function (e){
                $('#' + $(this).attr('target')).show();
            },
            function (e){
                $('#' + $(this).attr('target')).hide();
            }
        );

        // Placeholder shim.
        if ($.browser.msie) {
            $('input[placeholder], textarea[placeholder]').placeholder();
        }

        // Activate uniform UI.
        $(".js_uniform").uniform();

        // Newsletter signup form.
        $('.newsletter-form').submit(function(e) {
            e.preventDefault();

            var $form = $(this);
            $form.addClass('loading');
            $form.find('.fields').slideUp('fast', function() {
                $.ajax({
                    type: $form.attr('method'),
                    url: $form.attr('action'),
                    data: $form.serialize()
                }).done(function() {
                    $form.removeClass('loading');
                    $form.find('.success').slideDown('fast');
                });
            });
        });

        // Activate spinners.
        $('.spinner.small.white').spin({
            length: 3,
            width: 2,
            radius: 4,
            color: '#FFF',
            top: 0,
            left: 0,
            className: ''
        });
    });
})(jQuery, MonthYearPicker);
