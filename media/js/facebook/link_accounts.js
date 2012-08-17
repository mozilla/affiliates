(function($) {
    // Handle submission of the account linking form.
    $(document).on('submit', '#account-link-form', function(e) {
        e.preventDefault();

        var $form = $(this);
        var url = $form.attr('action');

        $.ajax({
            type: 'POST',
            url: url,
            data: $form.serialize()
        }).done(function() {
            $form.fadeOut(500, function() {
                $('#account-link-success').fadeIn(500);
            });
        });
    });
})($);