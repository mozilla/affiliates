(function($) {
    var FEED_URL = 'http://www.facebook.com/dialog/feed';

    // Redirect the frame to the Feed Dialog when a "Post to Wall" link is
    // clicked.
    $(document).on('click', '.post-to-wall', function(e) {
        e.preventDefault();

        var $link = $(this);
        var $body = $('body');
        var $banner_list = $('.banner-list');

        var params = $.param({
            app_id: $body.data('appId'),
            link: $body.data('fxDownloadUrl'),
            redirect_uri: $banner_list.data('feedRedirectUri'),
            picture: $link.data('img'),
            description: $link.data('text')
        });

        window.top.location = FEED_URL + '?' + params;
    });
})($);