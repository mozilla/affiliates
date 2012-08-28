(function($) {
    // Submit the filter form as soon as the country changes.
    $('#id_country').change(function() {
        $('#select-country').submit();
    });
})(jQuery);