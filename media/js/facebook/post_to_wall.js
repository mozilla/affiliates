(function($) {
    var FEED_URL = 'http://www.facebook.com/dialog/feed';

    // Redirect the frame to the Feed Dialog when a "Post to Wall" link is
    // clicked.
    $(document).on('click', '.share-banner', function(e) {
        e.preventDefault();

        // Link contains link-specific data, banner_list contains page-specific
        // data, and body contains site-wide data.
        var $share_link = $(this);
        var $banner_list = $('.banner-list');
        var $body = $('body');

        var params = $.param({
            app_id: $body.data('appId'),
            picture: $share_link.data('img'),
            description: $share_link.data('text'),
            link: $share_link.data('link'),
            redirect_uri: $banner_list.data('shareBannerRedirect')
        });

        window.top.location = FEED_URL + '?' + params;
    });
})($);