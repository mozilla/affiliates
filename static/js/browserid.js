(function() {

var form = $('#home-registration-forms');
var url = form.data('browserid-verify');
var csrf = form.data('csrf');
var msg_warning = $('#browserid-login .msg_warning');
var msg_no_assertion = form.data('browserid-no-assertion');
var msg_verify_fail = form.data('browserid-verify-fail');

function showBrowserIDError(msg) {
    return function() {
        msg_warning.text(msg);
        msg_warning.fadeIn(400);
    };
}

$('.persona-button').click(function(e) {
    e.preventDefault();

    var button = $(this).parent('.persona-button-container');
    var spinner = button.find('.spinner');
    spinner.addClass('visible');

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
                        $('#browserid-login').fadeOut(400, function() {
                            $('#browserid-registration').fadeIn(400);
                        });
                    }
                },
                statusCode: {
                    400: showBrowserIDError(msg_no_assertion),
                    403: showBrowserIDError(msg_verify_fail)
                },
                error: showBrowserIDError(msg_no_assertion),
                complete: function() {
                    spinner.removeClass('visible');
                }
            });
        }
    });
});

})();
