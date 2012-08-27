/**
 * Page Initialization
 */
$(
    function(event){
        HomePage.init();

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
    }
);

/**
 * Home Page Class
 */
var HomePage = {

    /**
     * Home Page Initialization
     */
    init: function(){
        HomePage.addEventListeners();
    },

    /**
     *
     */
    addEventListeners: function(){
        if ($(".js_no_action").length) {
            $(".js_no_action").click(function(e){
                e.preventDefault();
            });
        }
        if ($(".js_accordion").length) {
            $(".js_accordion").each(function(index, elem){
                HomePage.initAccordion(elem);
            });
        }
        if ($(".show_tooltip").length) {
            $(".show_tooltip").click(function(e){
                e.preventDefault();
            });
            $(".show_tooltip").hover(
                function(e){
                    HomePage.toggleToolTip($(this).attr('target'), e.type);
                },
                function(e){
                    HomePage.toggleToolTip($(this).attr('target'), e.type);
                });
        }
        if($.browser.msie) {
            $('input[placeholder], textarea[placeholder]').placeholder();
        }
        if ($(".js_uniform").length) {
            $(".js_uniform").uniform();
        }
    },
    toggleToolTip: function(target, e){
        var tooltip = $('#' + target);

        if (e == "mouseenter") {
            tooltip.show();
        } else {
            tooltip.hide();
        }
    },
    initAccordion : function(elem){
        var ulAccordion = $(elem),
            lnkAction = $("h5 a", ulAccordion),
            liElement, answerElement;

        ulAccordion.children().removeClass().addClass('collapsed');
        lnkAction.each(function(){
            $(this).click(function(e){
                e.preventDefault();
                liElement = $(this).parents('li');
                answerElement = $('.answer', liElement);
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
    }
};
