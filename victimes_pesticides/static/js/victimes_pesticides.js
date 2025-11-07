// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function() {
    const mobileMenuButton = document.getElementById('mobileMenuButton');
    const mobileNav = document.getElementById('mobileNav');

    if (mobileMenuButton && mobileNav) {
        mobileMenuButton.addEventListener('click', function() {
            mobileNav.classList.toggle('hidden');
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
            }
        });
    }
});
