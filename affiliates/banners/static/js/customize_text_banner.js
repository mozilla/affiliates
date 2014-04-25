/* global jQuery */
;(function($) {
    'use strict';

    var $form = $('#customize-banner-form');
    var $preview = $('#text-preview');
    var $submit = $form.find('button[type="submit"]');

    // When the variation selectbox changes, update the adjacent preview.
    $(document).on('change', '#customize-banner-form select[name="variation"]', function(e) {
        var $select = $(this);
        var variationsText = $form.data('variationsText');

        var text = variationsText[$select.val()];
        if (text) {
            $preview.text(text);
            $submit.prop('disabled', false);
        } else {
            $preview.text('');
            $submit.prop('disabled', true);
        }
    });

    // Trigger change event once on page load to populate.
    $(function() {
        $('#customize-banner-form select[name="variation"]').change();
    });
})(jQuery);
