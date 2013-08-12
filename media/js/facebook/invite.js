(function($) {
    var SEND_URL = 'http://www.facebook.com/dialog/send';

    // Redirect the frame to the Send Dialog.
    var $body = $('body');

    var params = $.param({
        app_id: $body.data('appId'),
        link: $body.data('link'),
        redirect_uri: $body.data('next')
    });

    window.top.location = SEND_URL + '?' + params;
})(jQuery);
