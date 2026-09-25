document.addEventListener('DOMContentLoaded', () => {
    const toggle = document.querySelector('.menu-toggle');
    const nav = document.querySelector('.nav-main');
    const dropdowns = document.querySelectorAll('.dropdown');

    if (toggle && nav) {
        toggle.addEventListener('click', () => {
            const isOpen = nav.classList.toggle('nav-open');
            toggle.setAttribute('aria-expanded', String(isOpen));
        });
    }

    dropdowns.forEach((dropdown) => {
        const button = dropdown.querySelector('.nav-dropdown-toggle');
        const menu = dropdown.querySelector('.nav-dropdown-menu');

        if (!button || !menu) return;

        button.addEventListener('click', (event) => {
            event.stopPropagation();

            dropdowns.forEach((otherDropdown) => {
                if (otherDropdown !== dropdown) {
                    otherDropdown.classList.remove('open');
                    const otherButton = otherDropdown.querySelector('.nav-dropdown-toggle');
                    if (otherButton) otherButton.setAttribute('aria-expanded', 'false');
                }
            });

            const isOpen = dropdown.classList.toggle('open');
            button.setAttribute('aria-expanded', String(isOpen));
        });

        menu.querySelectorAll('a').forEach((link) => {
            link.addEventListener('click', () => {
                dropdown.classList.remove('open');
                button.setAttribute('aria-expanded', 'false');
                if (window.innerWidth <= 768) {
                    if (nav) nav.classList.remove('nav-open');
                    if (toggle) toggle.setAttribute('aria-expanded', 'false');
                }
            });
        });
    });

    document.addEventListener('click', (event) => {
        dropdowns.forEach((dropdown) => {
            if (!dropdown.contains(event.target)) {
                dropdown.classList.remove('open');
                const button = dropdown.querySelector('.nav-dropdown-toggle');
                if (button) button.setAttribute('aria-expanded', 'false');
            }
        });
    });

    if (nav) {
        nav.querySelectorAll('a').forEach((link) => {
            link.addEventListener('click', () => {
                if (window.innerWidth <= 768) {
                    nav.classList.remove('nav-open');
                    if (toggle) toggle.setAttribute('aria-expanded', 'false');
                }
            });
        });
    }
});