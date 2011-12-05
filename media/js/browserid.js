$('a.browserid').click(function(e) {
    e.preventDefault();
    navigator.id.getVerifiedEmail(function(assertion) {
        if (assertion) {
            var form = $('#home-registration-forms'),
                url = form.data('browserid-verify'),
                csrf = form.data('csrf');
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
                error: function() {
                    alert('Error');
                }
            });
        }
    });
});
