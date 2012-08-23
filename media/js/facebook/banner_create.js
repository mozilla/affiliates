(function($) {
    $(document).ready(function() {
        // Set initial preview state if any form options are pre-checked
        var $radio = $(':radio[name="banner"]:checked');
        if ($radio.length > 0) {
            updatePreviewImage($radio);
        }

        // Show profile image preview if the option is pre-checked, or else hide
        $(':checkbox[name="use_profile_image"]').change();
    });

    // Swap the preview image as the selection changes
    $(':radio[name="banner"]').change(function() {
        updatePreviewImage($(this));
    });

    // Replaces the image in the banner preview with the one specified by the
    // given radio input.
    function updatePreviewImage($radio) {
        $('#banner').attr('src', $radio.data('image'));
        $(':radio[name="banner"]').parents('label').removeClass('selected');
        $radio.parents('label').addClass('selected');
    }

    // Show the note
    $('.note-link').click(function(e){
        e.preventDefault();
        $('#ad-note').fadeToggle('fast').removeAttr('aria-hidden');
    });

    // Hide note when anything else is clicked or focused on.
    $(document).on('click focus', function(e) {
        var $note = $('#ad-note');
        if ($note.is(':visible') &&
            $(e.target).is(':not(#ad-note, .note-link)')) {
            $note.fadeOut('fast').attr('aria-hidden', 'true');
        }
    });

    // Toggle the profile image preview when the option changes
    $(':checkbox[name="use_profile_image"]').change(function() {
        if ($(this).is(':checked')) {
            $('#userpic').fadeIn(100);
        }
        else {
            $('#userpic').fadeOut(100);
        }
    });

    // Handle submission of the form.
    var $form = $('#create-banner-form');
    $form.submit(function(e) {
        e.preventDefault();

        var url = $form.attr('action');
        $.ajax({
            type: 'POST',
            url: url,
            data: $form.serialize(),
            statusCode: {
                201: function(data) {
                    // 201 Created means the banner is created and we should
                    // redirect to the next step.
                    window.location = data.next;
                },
                202: function(data) {
                    // 202 Accepted means the banner is created and the app is
                    // generating a custom image for the banner. We should ping
                    // the server until the banner is done, then redirect to
                    // the next step.
                    $('.fm-submit .loading').show();
                    imageGenerationPing(data.check_url, data.next);
                }
            }
        });
    });

    function imageGenerationPing(check_url, next) {
        var ping = function() {
            $.ajax({
                type: 'GET',
                url: check_url
            }).done(function(data) {
                if (data.is_processed) {
                    window.location = next;
                } else {
                    setTimeout(ping, 3000);
                }
            });
        };

        ping();
    }

    // Special case: We need to know which button was used to submit the form,
    // so we need to override the default click behavior of the submit buttons.
    $('button[name="_next_action"]').click(function(e) {
        // Set the hidden input's value to the clicked button's value.
        $(':input[name="next_action"]').val($(this).val());
    });
})($);