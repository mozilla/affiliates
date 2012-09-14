(function($) {
    'use strict';

    var $banner_list = $('.banner-list');
    var confirmMsg = $banner_list.data('deleteConfirm');

    $banner_list.on('submit', '.delete-banner', function(e) {
        if (!window.confirm(confirmMsg)) {
            e.preventDefault();
        }
    });
})(jQuery);