/* This Source Code Form is subject to the terms of the Mozilla Public
 * License, v. 2.0. If a copy of the MPL was not distributed with this
 * file, You can obtain one at http://mozilla.org/MPL/2.0/. */

(function($) {
    'use strict';
    var $window = $(window);
    var $document = $(document);
    var $body = $('body');
    var $navList = $('#nav-main-menu');
    var $navListSub = $('#nav-user-submenu');

    // Add a class to use as a style hook when JavaScript is available
    $body.removeClass('no-js').addClass('js');

    // Trigger the .thin-mode class on <body> when the screen is thinner than
    // 760 pixels.
    $window.resize(function() {
        clearTimeout(this.resizeTimeoutId);
        this.resizeTimeoutId = setTimeout(doneResizing, 200);
    });

    function doneResizing() {
        if ($window.width() < 760) {
            $body.removeClass('wide-mode').addClass('thin-mode');
            $navList.attr('aria-hidden', 'true').hide();
        } else {
            $body.removeClass('thin-mode').addClass('wide-mode');
            $navList.removeAttr('aria-hidden').show();
        }
        $navListSub.removeAttr('style');
    }
    $(doneResizing);  // Call once when done loading the page to initialize.

    // Show/hide the main navigation in small viewports
    $document.on('click', '.thin-mode #nav-main .toggle', expandMainNav);
    $document.on('click', '.thin-mode #nav-main .toggle.open', collapseMainNav);
    $document.on('mouseleave', '.thin-mode #nav-main', collapseMainNav);

    function expandMainNav() {
        $navList.slideDown('fast').removeAttr('aria-hidden').attr('aria-expanded', 'true');
        $("#nav-main .toggle").addClass("open");
    }

    function collapseMainNav() {
        $navList.slideUp('fast').attr('aria-hidden', 'true').removeAttr('aria-expanded');
        $("#nav-main .toggle").removeClass("open");
    }

    // Show/hide the sub-navigation in wide viewports
    $document.on('mouseover', '.wide-mode #nav-main .user', expandSubNav);
    $document.on('click focus', '.wide-mode #nav-main .user > a', function(e) {
        e.preventDefault();
        expandSubNav();
    });
    $document.on('mouseleave', '.wide-mode #nav-main .user', collapseSubNav);

    function expandSubNav() {
        $navListSub.slideDown('fast').removeAttr('aria-hidden').attr('aria-expanded', 'true');
        $("#nav-main .user").addClass("open");
    }

    function collapseSubNav() {
        $navListSub.slideUp('fast').attr('aria-hidden', 'true').removeAttr('aria-expanded');
        $("#nav-main .user").removeClass("open");
    }

})(jQuery);
