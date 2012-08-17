(function($) {
    // Handle submission of the account linking form.
    $(document).on('submit', '#link-account', function(e) {
        e.preventDefault();

        var $form = $(this);
        var url = $form.attr('action');

        $.ajax({
            type: 'POST',
            url: url,
            data: $form.serialize()
        }).done(function() {
            $form.find('.form').fadeOut(500, function() {
                $form.find('.success-msg').fadeIn(500);
            });
        });
    });

    // Show/hide the account linking form
    $(".not-linked a").click(function(e){
        e.preventDefault();
        $("#link-account").slideToggle('fast');
        $(this).blur();
    });
})($);