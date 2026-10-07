function closeMobileMenu() {
    const btn = document.getElementById('mobile-menu-button');
    const menu = document.getElementById('mobile-menu');

    if (!btn || !menu) {
        return;
    }

    menu.classList.add('hidden');
    btn.setAttribute('aria-expanded', 'false');
}

function initMobileMenu() {
    // Delegated listeners on document survive body swaps and history
    // restores (which bring back DOM snapshots without event listeners).
    // The window flag prevents duplicates when HTMX re-runs this script.
    if (window.mobileMenuInitialized) {
        return;
    }

    window.mobileMenuInitialized = true;

    document.addEventListener('click', (evt) => {
        const btn = evt.target.closest('#mobile-menu-button');
        const menu = document.getElementById('mobile-menu');

        if (!btn || !menu) {
            return;
        }

        const isHidden = menu.classList.toggle('hidden');

        btn.setAttribute(
            'aria-expanded',
            String(!isHidden)
        );
    });

    document.body.addEventListener('htmx:beforeHistorySave', closeMobileMenu);
    document.body.addEventListener('htmx:historyRestore', closeMobileMenu);
    window.addEventListener('pageshow', (evt) => {
        if (evt.persisted) {
            closeMobileMenu();
        }
    });
}


initMobileMenu();


function initSpaNavigation() {
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
