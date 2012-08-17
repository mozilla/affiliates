(function($) {
    $(document).ready(function() {
        // Set initial preview state if any form options are pre-checked
        var $radio = $(':radio[name="banner"]:checked');
        if ($radio.length > 0) {
            updatePreviewImage($radio);
        }

        // Show profile image preview if the option is pre-checked, or else hide
        $('#profile-img').change();
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
    $('#profile-img').change(function() {
        if ($(this).is(':checked')) {
            $('#userpic').fadeIn(100);
        }
        else {
            $('#userpic').fadeOut(100);
        }
    });

})($);