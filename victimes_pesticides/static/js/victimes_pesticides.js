// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuButton = document.getElementById('mobileMenuButton');
    const mobileNav = document.getElementById('mobileNav');

    if (mobileMenuButton && mobileNav) {
        mobileMenuButton.addEventListener('click', function() {
            mobileNav.classList.toggle('hidden');
            const expanded = !mobileNav.classList.contains('hidden');
            mobileMenuButton.setAttribute('aria-expanded', expanded);
            mobileMenuButton.setAttribute('aria-label', expanded ? 'Fermer le menu' : 'Ouvrir le menu');
        });

        // Close mobile menu when clicking on a link
        const mobileLinks = mobileNav.querySelectorAll('a');
        mobileLinks.forEach(function(link) {
            link.addEventListener('click', function() {
                mobileNav.classList.add('hidden');
            });
        });

        // Close mobile menu when clicking outside
        document.addEventListener('click', function(event) {
            const isClickInsideNav = mobileNav.contains(event.target);
            const isClickOnButton = mobileMenuButton.contains(event.target);

            if (!isClickInsideNav && !isClickOnButton && !mobileNav.classList.contains('hidden')) {
                mobileNav.classList.add('hidden');
                mobileMenuButton.setAttribute('aria-expanded', 'false');
                mobileMenuButton.setAttribute('aria-label', 'Ouvrir le menu');
            }
        });
    }

    // Accordion Toggle
    const accordeonToggles = document.querySelectorAll('.accordeon-toggle');

    function getAccordeonContent(toggle) {
        const targetId = toggle.getAttribute('data-target');
        const accordeonItem = toggle.closest('.accordeon-item');
        return accordeonItem ? accordeonItem.querySelector('.accordeon-content') : document.getElementById(targetId);
    }

    function setAccordeonExpanded(toggle, expanded) {
        const content = getAccordeonContent(toggle);
        const icon = toggle.querySelector('.accordeon-icon');

        if (content) {
            content.classList.toggle('hidden', !expanded);
            toggle.setAttribute('aria-expanded', expanded ? 'true' : 'false');
            if (icon) {
                icon.classList.toggle('rotate-180', expanded);
            }
        }
    }

    function openAccordeonFromHash() {
        if (!window.location.hash) {
            return;
        }

        let targetId = window.location.hash.substring(1);
        try {
            targetId = decodeURIComponent(targetId);
        } catch (error) {
            // Keep the raw hash if decoding fails.
        }

        const target = document.getElementById(targetId);
        const accordeonItem = target && target.classList.contains('accordeon-item') ? target : target?.closest('.accordeon-item');
        const toggle = accordeonItem ? accordeonItem.querySelector('.accordeon-toggle') : null;

        if (toggle) {
            setAccordeonExpanded(toggle, true);
            window.requestAnimationFrame(function() {
                accordeonItem.scrollIntoView({ block: 'start' });
            });
        }
    }

    accordeonToggles.forEach(function(toggle) {
        // Set initial ARIA state
        toggle.setAttribute('aria-expanded', 'false');
        toggle.addEventListener('click', function() {
            const content = getAccordeonContent(this);
            const expanded = content ? content.classList.contains('hidden') : false;
            setAccordeonExpanded(this, expanded);
        });
    });

    openAccordeonFromHash();
    window.addEventListener('hashchange', openAccordeonFromHash);
});
