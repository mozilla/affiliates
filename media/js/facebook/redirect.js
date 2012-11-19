(function() {
    var target = window;
    var $body = $(document.body);
    if ($body.data('topWindow')) {
        target = window.top;
    }

    target.location = $body.data('url');
})();
