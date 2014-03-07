/* global jQuery */
;(function($) {
    'use strict';

    // When the variation selectbox changes, update the adjacent preview.
    $(document).on('change', '#customize-banner-form select[name="variation"]', function(e) {
        var $select = $(this);
        var variationsText = $select.parent('#customize-banner-form').data('variationsText');
        var $preview = $select.siblings('.preview');

        $preview.text(variationsText[$select.val()]);
    });

    // Trigger change event once on page load to populate.
    $(function() {
        $('#customize-banner-form select[name="variation"]').change();
    });
})(jQuery);
