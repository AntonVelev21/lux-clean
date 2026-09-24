function initMobileMenu() {
    const btn = document.getElementById('mobile-menu-button');
    const menu = document.getElementById('mobile-menu');

    if (!btn || !menu) {
        return;
    }

    // Prevent duplicate listeners.
    if (btn.dataset.menuInitialized === 'true') {
        return;
    }

    btn.dataset.menuInitialized = 'true';

    btn.addEventListener('click', () => {
        const isHidden = menu.classList.toggle('hidden');

        btn.setAttribute(
            'aria-expanded',
            String(!isHidden)
        );
    });
}


// Runs at script-execution time: on the real page load this fires after the
// DOM above it has parsed, and htmx re-runs this whole script on every
// hx-boost swap (it lives inside the swapped body), so a direct call covers
// both cases without depending on event timing.
initMobileMenu();


function initSpaNavigation() {
    // document.body survives every hx-boost swap (only its children are
    // replaced), so guard registration on it rather than on this script's
    // re-execution, which would otherwise pile up duplicate listeners.
    if (document.body.dataset.spaNavInitialized === 'true') {
        return;
    }

    document.body.dataset.spaNavInitialized = 'true';

    document.body.addEventListener('htmx:beforeRequest', (evt) => {
        if (!evt.detail.boosted) {
            return;
        }

        const bar = document.getElementById('page-loading-bar');
        if (!bar) {
            return;
        }

        bar.classList.remove('is-done');
        bar.classList.add('is-loading');
    });

    const finishLoadingBar = (evt) => {
        if (!evt.detail.boosted) {
            return;
        }

        // The loading bar element itself gets replaced by the swap, so look
        // up whichever instance is live right now instead of caching one.
        const bar = document.getElementById('page-loading-bar');
        if (!bar) {
            return;
        }

        bar.classList.remove('is-loading');
        bar.classList.add('is-done');

        setTimeout(() => {
            bar.classList.remove('is-done');
        }, 300);
    };

    document.body.addEventListener('htmx:afterRequest', finishLoadingBar);
    document.body.addEventListener('htmx:responseError', finishLoadingBar);
    document.body.addEventListener('htmx:sendError', finishLoadingBar);

    document.body.addEventListener('htmx:afterSettle', (evt) => {
        if (!evt.detail.boosted) {
            return;
        }

        window.scrollTo({ top: 0, behavior: 'auto' });
    });
}


initSpaNavigation();
