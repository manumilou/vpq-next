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
    accordeonToggles.forEach(function(toggle) {
        // Set initial ARIA state
        toggle.setAttribute('aria-expanded', 'false');
        toggle.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const accordeonItem = this.closest('.accordeon-item');
            const content = accordeonItem ? accordeonItem.querySelector('.accordeon-content') : document.getElementById(targetId);
            const icon = this.querySelector('.accordeon-icon');

            if (content) {
                content.classList.toggle('hidden');
                const expanded = !content.classList.contains('hidden');
                this.setAttribute('aria-expanded', expanded);
                if (icon) {
                    icon.classList.toggle('rotate-180');
                }
            }
        });
    });
});
