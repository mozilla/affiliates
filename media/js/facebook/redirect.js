(function() {
    var target = window;
    if (document.body.dataset.topWindow) {
        target = window.top;
    }

    target.location = document.body.dataset.url;
})();
