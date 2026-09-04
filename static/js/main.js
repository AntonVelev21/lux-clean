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
