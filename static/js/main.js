// static/js/main.js
document.addEventListener('DOMContentLoaded', () => {
    // Логика за мобилното меню в навигацията
    const btn = document.getElementById('mobile-menu-button');
    const menu = document.getElementById('mobile-menu');

    if (btn && menu) {
        btn.addEventListener('click', () => {
            menu.classList.toggle('hidden');
        });
    }
});

// Логика за Scroll Reveal анимациите
const revealElements = document.querySelectorAll('.reveal-on-scroll');

// Настройки на обзървъра (появява се, когато картата е 10% видима)
const revealOptions = {
    threshold: 0.1,
    rootMargin: "0px 0px -50px 0px"
};

const revealObserver = new IntersectionObserver(function(entries, observer) {
    entries.forEach(entry => {
        if (!entry.isIntersecting) {
            return;
        } else {
            entry.target.classList.add('is-visible');
            // Спираме да наблюдаваме елемента, след като вече се е появил
            observer.unobserve(entry.target);
        }
    });
}, revealOptions);

revealElements.forEach(el => {
    revealObserver.observe(el);
});