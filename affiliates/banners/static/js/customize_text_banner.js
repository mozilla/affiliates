/* global jQuery */
;(function($) {
    'use strict';

    var $form = $('#customize-banner-form');

    // When the variation selectbox changes, update the adjacent preview.
    $(document).on('change', '#customize-banner-form select[name="variation"]', function(e) {
        var $select = $(this);
        var variationsText = $form.data('variationsText');
        var $preview = $('#text-preview');

        $preview.text(variationsText[$select.val()]);
    });

    // Trigger change event once on page load to populate.
    $(function() {
        $('#customize-banner-form select[name="variation"]').change();
    });
})(jQuery);
