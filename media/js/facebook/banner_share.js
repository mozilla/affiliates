(function($) {
    var FEED_URL = 'http://www.facebook.com/dialog/feed';

    // Redirect the frame to the Feed Dialog.
    var $body = $('body');

    var params = $.param({
        app_id: $body.data('appId'),
        picture: $body.data('img'),
        description: $body.data('text'),
        link: $body.data('link'),
        redirect_uri: $body.data('next')
    });

    window.top.location = FEED_URL + '?' + params;
})($);