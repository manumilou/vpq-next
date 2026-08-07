// Mobile Menu Toggle + accordions
(function() {
    function onReady(callback) {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', callback);
        } else {
            callback();
        }
    }

    function hasClass(element, className) {
        return element && element.classList && element.classList.contains(className);
    }

    function toggleClass(element, className, shouldAdd) {
        if (!element || !element.classList) {
            return;
        }

        if (shouldAdd) {
            element.classList.add(className);
        } else {
            element.classList.remove(className);
        }
    }

    function closestByClass(element, className) {
        while (element && element !== document) {
            if (hasClass(element, className)) {
                return element;
            }
            element = element.parentNode;
        }
        return null;
    }

    onReady(function() {
        var mobileMenuButton = document.getElementById('mobileMenuButton');
        var mobileNav = document.getElementById('mobileNav');

        if (mobileMenuButton && mobileNav) {
            mobileMenuButton.addEventListener('click', function() {
                mobileNav.classList.toggle('hidden');
                var expanded = !mobileNav.classList.contains('hidden');
                mobileMenuButton.setAttribute('aria-expanded', expanded ? 'true' : 'false');
                mobileMenuButton.setAttribute('aria-label', expanded ? 'Fermer le menu' : 'Ouvrir le menu');
            });

            // Close mobile menu when clicking on a link
            var mobileLinks = mobileNav.querySelectorAll('a');
            for (var i = 0; i < mobileLinks.length; i++) {
                mobileLinks[i].addEventListener('click', function() {
                    mobileNav.classList.add('hidden');
                });
            }

            // Close mobile menu when clicking outside
            document.addEventListener('click', function(event) {
                var isClickInsideNav = mobileNav.contains(event.target);
                var isClickOnButton = mobileMenuButton.contains(event.target);

                if (!isClickInsideNav && !isClickOnButton && !mobileNav.classList.contains('hidden')) {
                    mobileNav.classList.add('hidden');
                    mobileMenuButton.setAttribute('aria-expanded', 'false');
                    mobileMenuButton.setAttribute('aria-label', 'Ouvrir le menu');
                }
            });
        }

        // Accordion Toggle
        var accordeonToggles = document.querySelectorAll('.accordeon-toggle');

        function getAccordeonContent(toggle) {
            var targetId = toggle.getAttribute('data-target');
            var accordeonItem = closestByClass(toggle, 'accordeon-item');
            var content = accordeonItem ? accordeonItem.querySelector('.accordeon-content') : null;

            if (!content && targetId) {
                content = document.getElementById(targetId);
            }

            return content;
        }

        function setAccordeonExpanded(toggle, expanded) {
            var content = getAccordeonContent(toggle);
            var icon = toggle.querySelector('.accordeon-icon');

            if (content) {
                toggleClass(content, 'hidden', !expanded);
                toggle.setAttribute('aria-expanded', expanded ? 'true' : 'false');
                toggleClass(icon, 'rotate-180', expanded);
            }
        }

        function openAccordeonFromHash() {
            if (!window.location.hash) {
                return;
            }

            var targetId = window.location.hash.substring(1);
            try {
                targetId = decodeURIComponent(targetId);
            } catch (error) {
                // Keep the raw hash if decoding fails.
            }

            var target = document.getElementById(targetId);
            var accordeonItem = null;

            if (target) {
                accordeonItem = hasClass(target, 'accordeon-item') ? target : closestByClass(target, 'accordeon-item');
            }

            var toggle = accordeonItem ? accordeonItem.querySelector('.accordeon-toggle') : null;

            if (toggle) {
                setAccordeonExpanded(toggle, true);
                var scrollToAccordeon = function() {
                    accordeonItem.scrollIntoView(true);
                };

                if (window.requestAnimationFrame) {
                    window.requestAnimationFrame(scrollToAccordeon);
                } else {
                    scrollToAccordeon();
                }
            }
        }

        for (var j = 0; j < accordeonToggles.length; j++) {
            // Set initial ARIA state
            accordeonToggles[j].setAttribute('aria-expanded', 'false');
            accordeonToggles[j].addEventListener('click', function() {
                var content = getAccordeonContent(this);
                var expanded = content ? content.classList.contains('hidden') : false;
                setAccordeonExpanded(this, expanded);
            });
        }

        openAccordeonFromHash();
        window.addEventListener('hashchange', openAccordeonFromHash);
    });
})();
