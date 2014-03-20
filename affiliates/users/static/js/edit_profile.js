;(function($) {
    'use strict';

    var $doc = $(document);
    $doc.on('click', '#edit-profile-link', function(e) {
        e.preventDefault();

        $('#edit-profile-popup').show();
    });

    $doc.on('click', '#edit-profile-popup .close', function(e) {
        e.preventDefault();

        $(this).parents('#edit-profile-popup').hide();
    });
})(jQuery);
