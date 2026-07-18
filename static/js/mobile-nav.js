/**
 * Off-canvas mobile menu — slides in smoothly from the right,
 * replacing the old top-down accordion dropdown.
 */
(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        var toggle = document.getElementById('mobileMenuToggle');
        var menu = document.getElementById('offcanvasMenu');
        var overlay = document.getElementById('offcanvasOverlay');
        var closeBtn = document.getElementById('offcanvasClose');

        if (!toggle || !menu || !overlay || !closeBtn) return;

        function openMenu() {
            menu.classList.add('is-open');
            overlay.classList.add('is-open');
            document.body.classList.add('offcanvas-open');
        }

        function closeMenu() {
            menu.classList.remove('is-open');
            overlay.classList.remove('is-open');
            document.body.classList.remove('offcanvas-open');
        }

        toggle.addEventListener('click', openMenu);
        closeBtn.addEventListener('click', closeMenu);
        overlay.addEventListener('click', closeMenu);

        // Close automatically when a real link inside the menu is clicked
        menu.querySelectorAll('a').forEach(function (link) {
            link.addEventListener('click', function () {
                if (!link.classList.contains('js-doc-view')) closeMenu();
            });
        });

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && menu.classList.contains('is-open')) closeMenu();
        });
    });
})();
