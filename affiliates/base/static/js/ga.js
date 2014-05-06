var _gaAccountCode = document.documentElement.getAttribute('data-ga-code');

var _gaq = _gaq || [];
_gaq.push(['_setAccount', _gaAccountCode]);
_gaq.push(['_trackPageview']);

if (_gaAccountCode) {
    (function() {
        var ga = document.createElement('script');
        ga.type = 'text/javascript';
        ga.async = true;
        ga.src = 'https://ssl.google-analytics.com/ga.js';
        var s = document.getElementsByTagName('script')[0];
        s.parentNode.insertBefore(ga, s);
    })();
}
