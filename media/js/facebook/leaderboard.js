(function($) {
    // Submit the filter form as soon as the country changes.
    $('#id_country').change(function() {
        $('form.select-country').submit();
    });
})(jQuery);