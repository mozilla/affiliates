$(function() {
    var $preview = $('#preview'),
        $size = $('#size'),
        $color = $('#color'),
        $language = $('#language'),
        $form_image = $('#id_image'),
        banner_images = $preview.data('images'),
        banner_alt = $preview.data('alt'),
        banner_template = '<img src="{{ img }}" alt="{{ alt }}">';

    // Populate a select dropdown
    function set_options($list, options) {
        $list.empty();
        for (var k = 0; k < options.length; k++) {
            $list.append('<option value="' + options[k] + '">' + options[k] +
                         '</option>');
        }
    }

    // Update the banner preview to match the current options
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
            $preview.html(Mustache.to_html(banner_template, {
                img: image.url,
                alt: banner_alt
            }));
            $form_image.val(image.pk);
        }
    }

    // Populate the languages dropdown
    var languages = _(banner_images).chain()
            .map(function(img){return img.language;})
            .uniq().value();
    set_options($language, languages);
    $language.val($('html').data('language'));
    $.uniform.update();

    // When language changes, populate the size dropdown
    $language.change(function(e) {
        var lang = $language.val(),
            sizes = _(banner_images).chain()
                .filter(function(img){return img.language === lang;})
                .sortBy(function(img) { return img.area; })
                .map(function(img){return img.size;})
                .uniq(true) // true = already sorted = faster algorithm
                .value();

        set_options($size, sizes);
        $size.change();
    }).change();

    // When size changes, populate the color dropdown
    $size.change(function(e) {
        var size = $size.val(),
            lang = $language.val(),
            colors = _(banner_images).chain()
                .filter(function(img) {return img.size === size &&
                                       img.language === lang;})
                .map(function(img) { return img.color; })
                .sortBy(_.identity)
                .uniq(true)
                .value();

        set_options($color, colors);
        $.uniform.update();
        update_image();
    }).change();

    // When color changes... update the image.
    $color.change(function(e) {
        update_image();
    });
});
