$(function() {
    function set_options($list, options) {
        $list.empty();
        for (var k = 0; k < options.length; k++) {
            $list.append('<option value="' + options[k] + '">' + options[k] +
                         '</option>');
        }
    }

    var $preview = $('#banner_preview'),
        $badge_code = $('#badge_code'),
        $size = $('#size'),
        $color = $('#color'),
        $language = $('#language'),
        banner_images = $preview.data('images');

    function generate_affiliate_url(banner_img_id) {
        return Mustache.to_html($preview.data('affiliate-link'),
                                {banner_img_id: banner_img_id});
    }

    function update_image() {
        var language = $language.val(),
            size = $size.val(),
            color = $color.val();

        var image = _.find(banner_images, function(img) {
            return img.color === color
                && img.size === size
                && img.language === language;
        });

        if (image !== undefined) {
            var banner = Mustache.to_html($preview.data('template'), {
                url: generate_affiliate_url(image.pk),
                img: image.url
            });

            $preview.html(banner);
            $badge_code.val(banner);
        }
    }

    var languages = _(banner_images).chain()
            .map(function(img){return img.language;})
            .uniq().value();
    set_options($language, languages);
    $language.val($('html').data('language'));
    $.uniform.update();

    $language.change(function(e) {
        var val = $language.val(),
            sizes = _(banner_images).chain()
                .filter(function(img){return img.language === val;})
                .map(function(img){return img.size;})
                .uniq().value();

        set_options($size, sizes);
        $.uniform.update();
        update_image();
    }).change();

    $size.change(function(e) {
        var val = $size.val(),
            colors = _(banner_images).chain()
                .filter(function(img) {return img.size === val;})
                .map(function(img) { return img.color; })
                .uniq().value();

        set_options($color, colors);
        $.uniform.update();
        update_image();
    }).change();

    $color.change(function(e) {
        update_image();
    });
});
