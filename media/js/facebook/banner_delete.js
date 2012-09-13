(function($) {
    'use strict';

    var confirmMsg = $('.banner-list').data('deleteConfirm');

    $(document).on('click', '.delete-banner', function(e) {
        e.preventDefault();
        if (window.confirm(confirmMsg)) {
            $(e.target).parent('form').submit();
        }
    });
})(jQuery);