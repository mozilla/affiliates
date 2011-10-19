$(function() {
    // TODO: Support multiple levels
    function make_select_dependent(parent, child, choices) {
        var $parent = $(parent), $child = $(child);

        for (var choice in choices) {
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
                    $child.append('<option value="'+child_choices[k]+'">' +
                                  child_choices[k]+'</option>');
                }
            }
            $.uniform.update();
        }).change();
    }

    var preview = $('#banner_preview'),
        badge_code = $('#badge_code'),
        size = $('#size'),
        color = $('#color'),
        banner_images = preview.data('images'),
        template = preview.data('template');

    make_select_dependent(size, color, size.data('choices'));

    function generate_affiliate_url(banner_img_id) {
        return Mustache.to_html(preview.data('affiliate-link'),
                                {banner_img_id: banner_img_id});
    }

    size.add(color).change(function(e) {
        var banner_img = banner_images[size.val()][color.val()];
        var url = generate_affiliate_url(banner_img['pk']);
        var banner = Mustache.to_html(preview.data('template'), {
            url: url,
            img: banner_img['image_url']
        });
        
        preview.html(banner);
        badge_code.val(banner);
    }).change();
});
