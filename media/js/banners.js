$(function() {
    // TODO: Support multiple levels
    function make_select_dependent(parent, child, choices) {
        var $parent = $(parent), $child = $(child);

        for (choice in choices) {
            if (choices.hasOwnProperty(choice)) {
                $parent.append('<option value="'+choice+'">'+choice+'</option>');
            }
        }

        $parent.change(function(e) {
            var self = $(this);
            if (choices[self.val()] instanceof Array) {
                var child_choices = choices[self.val()];
                $child.empty();
                for (var k = 0; k < child_choices.length; k++) {
                    $child.append('<option value="'+child_choices[k]+'">'
                                  +child_choices[k]+'</option>');
                }
            }
        }).change();
    }

    function str_format(str) {
        for (var k = 1; k < arguments.length; k++) {
            str = str.replace('%s', arguments[k]);
        }

        return str;
    }

    var preview = $('#banner_preview'),
        badge_code = $('#badge_code'),
        size = $('#size'),
        color = $('#color'),
        banner_images = preview.data('images'),
        template = preview.data('template');
    make_select_dependent(size, color, size.data('choices'));
    size.add(color).change(function(e) {
        var img = banner_images[size.val()][color.val()];
        var banner = str_format(template, '#', img, '');
        preview.html(banner);
        badge_code.val(banner);
    }).change();
});
