$(function() {
    var $preview = $('#banner_preview'),
        $size = $('#size'),
        $color = $('#color'),
        $language = $('#language'),
        banner_images = $preview.data('images');

    function set_options($list, options) {
        $list.empty();
        for (var k = 0; k < options.length; k++) {
            $list.append('<option value="' + options[k] + '">' + options[k] +
                         '</option>');
        }
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
            $preview.html(Mustache.to_html('<img src="{{ img }}">', {
                img: image.url
            }));
        }
    }

    var languages = _(banner_images).chain()
            .map(function(img){return img.language;})
            .uniq().value();
    set_options($language, languages);
    $language.val($('html').data('language'));
    $.uniform.update();

    $language.change(function(e) {
        var lang = $language.val(),
            sizes = _(banner_images).chain()
                .filter(function(img){return img.language === lang;})
                .map(function(img){return img.size;})
                .uniq().value();

        set_options($size, sizes);
        $size.change();
    }).change();

    $size.change(function(e) {
        var size = $size.val(),
            lang = $language.val(),
            colors = _(banner_images).chain()
                .filter(function(img) {return img.size === size &&
                                       img.language === lang;})
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
