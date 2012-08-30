(function($) {
    // Handle submission of the account linking form.
    $('#link-account').submit(function(e) {
        e.preventDefault();

        var $form = $(this);
        var url = $form.attr('action');

        $.ajax({
            type: 'POST',
            url: url,
            data: $form.serialize()
        }).done(function() {
            $form.find('.form').fadeOut(500, function() {
                $form.find('.success-msg').fadeIn(500);
            });
        });
    });

    // Show/hide the account linking form
    $(".not-linked a").click(function(e){
        e.preventDefault();
        $("#link-account").slideToggle('fast');
        $(this).blur();
    });

    // Common startup options.
    $(document).ready(function() {
        // Hide newsletter options
        $("#newsletter .options").hide();

        // Activate FAQ sliders.
        FAQ.init();

        // Activate spinners.
        $('.spinner').spin();
    });

    // Show newsletter options
    $("#newsletter_email").focus(function(){
        $("#newsletter .options").slideDown('fast');
    });

    // Handle submission of the newsletter form.
    // TODO: Handle errors!
    $('#newsletter-form').submit(function(e) {
        e.preventDefault();

        var $form = $(this);
        $.ajax({
            type: $form.attr('method'),
            url: $form.attr('action'),
            data: $form.serialize()
        }).done(function() {
            $form.slideUp('fast', function() {
                $('#newsletter-success').slideDown('fast');
            });
        });
    });

    // Initialize MonthYearPicker
    var monthYearPicker = new MonthYearPicker('.month-year-picker', {
        errorMsgSelector: '.stats-warning'
    });
    monthYearPicker.onRefresh(function(data) {
        $('#total-clicks').text(data.clicks);
    });
})(jQuery);

/**
 * FAQ Page Class
 */
var FAQ = {
    init: function(){
        FAQ.addEventListeners();
    },

    addEventListeners: function(){
        $(".js_accordion").each(function(index, elem){
            FAQ.initAccordion(elem);
        });
    },

    initAccordion : function(elem){
        var ulAccordion = $(elem);
        var lnkAction = $("h4 a", ulAccordion);
        var liElement;
        var answerElement;

        ulAccordion.children().removeClass().addClass('collapsed');
        lnkAction.click(function(e){
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
    }

};