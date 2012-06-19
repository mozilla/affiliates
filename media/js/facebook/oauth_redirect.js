(function() {
    var app_id = document.body.dataset.appId;
    var app_namespace = document.body.dataset.appNamespace;
    var permissions = document.body.dataset.permissions;

    var oauth_url = 'https://www.facebook.com/dialog/oauth/';
    oauth_url += '?client_id=' + app_id;
    oauth_url += ('&redirect_uri=' +
                  encodeURIComponent('https://apps.facebook.com/' +
                                     app_namespace + '/'));
    oauth_url += '&scope=' + permissions;

    window.top.location = oauth_url;
})();