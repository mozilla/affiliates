(function($) {
    var $body = $('body');
    var app_id = $body.data('appId');
    var app_namespace = $body.data('appNamespace');
    var permissions = $body.data('permissions');

    var oauth_url = 'https://www.facebook.com/dialog/oauth/';
    oauth_url += '?client_id=' + app_id;
    oauth_url += ('&redirect_uri=' +
                  encodeURIComponent('https://apps.facebook.com/' +
                                     app_namespace + '/'));
    oauth_url += '&scope=' + permissions;

    $body.on('click', '#request-authorization', function(e) {
        e.preventDefault();
        window.top.location = oauth_url;
    });
})(jQuery);
