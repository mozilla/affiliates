(function($) {
    var SEND_URL = 'http://www.facebook.com/dialog/send';

    // Redirect the frame to the Send Dialog.
    var $body = $('body');

    var params = $.param({
        app_id: $body.data('appId'),
        picture: $body.data('picture'),
        name: $body.data('name'),
        description: $body.data('description'),
        link: $body.data('link'),
        redirect_uri: $body.data('next')
    });

    window.top.location = SEND_URL + '?' + params;
})(jQuery);