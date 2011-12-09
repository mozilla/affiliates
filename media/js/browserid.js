(function() {

var form = $('#home-registration-forms'),
    url = form.data('browserid-verify'),
    csrf = form.data('csrf'),
    msg_no_assertion = form.data('browserid-no-assertion'),
    msg_verify_fail = form.data('browserid-verify-fail');

function showBrowserIDError(msg) {
    return function() {
        form.find('p.msg_warning').empty();
        $('<p class="msg_warning">' + msg + '</p>')
            .hide()
            .prependTo(form)
            .fadeIn(400);
    };
}

$('a.browserid').click(function(e) {
    e.preventDefault();
    navigator.id.getVerifiedEmail(function(assertion) {
        if (assertion) {
            $.ajax({
                url: url,
                type: 'POST',
                data: {assertion: assertion, csrfmiddlewaretoken: csrf},
                success: function(data) {
                    if (data.registered) {
                        window.location.href = data.redirect;
                    } else {
                        $('#id_assertion').val(assertion);
                        $('#browserid-login').fadeOut(400, function() {
                            $('#browserid-registration').fadeIn(400);
                        });
                    }
                },
                statusCode: {
                    400: showBrowserIDError(msg_no_assertion),
                    403: showBrowserIDError(msg_verify_fail)
                },
                error: showBrowserIDError(msg_no_assertion)
            });
        }
    });
});

})();
