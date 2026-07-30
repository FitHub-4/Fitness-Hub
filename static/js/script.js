(function () {
    // Theme toggle
    (function initTheme() {
        const saved = localStorage.getItem('fh-theme');
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        const theme = saved || (prefersDark ? 'dark' : 'light');
        document.documentElement.setAttribute('data-theme', theme);
    })();

    function setThemeIcon() {
        const theme = document.documentElement.getAttribute('data-theme');
        document.querySelectorAll('.theme-toggle').forEach(function (btn) {
            btn.textContent = theme === 'dark' ? '\u2600' : '\u263E';
        });
    }

    document.addEventListener('click', function (e) {
        const btn = e.target.closest('.theme-toggle');
        if (!btn) return;
        const current = document.documentElement.getAttribute('data-theme');
        const next = current === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('fh-theme', next);
        setThemeIcon();
    });

    setThemeIcon();
    const menuToggle = document.getElementById('menuToggle');
    const mainNav = document.getElementById('mainNav');

    function closeMenu() {
        if (!menuToggle || !mainNav) return;
        mainNav.classList.remove('open');
        menuToggle.classList.remove('active');
        menuToggle.setAttribute('aria-expanded', 'false');
    }

    if (menuToggle && mainNav) {
        menuToggle.addEventListener('click', () => {
            const open = mainNav.classList.toggle('open');
            menuToggle.classList.toggle('active', open);
            menuToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
        });

        // Close menu on any nav link click (for mobile)
        mainNav.querySelectorAll('a, button').forEach((el) => {
            el.addEventListener('click', () => {
                if (window.innerWidth <= 992) {
                    closeMenu();
                }
            });
        });

        // Close menu on Escape key
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape' && mainNav.classList.contains('open')) {
                closeMenu();
            }
        });
    }

    const header = document.getElementById('siteHeader');
    if (header) {
        const onScroll = () => header.classList.toggle('is-scrolled', window.scrollY > 8);
        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
    }

    window.addEventListener('load', () => {
        document.body.dataset.loaded = 'true';
    });

    document.addEventListener('click', (e) => {
        const toggle = e.target.closest('.form-toggle');
        if (!toggle) return;
        const card = toggle.closest('.exercise-card');
        if (!card) return;
        const guide = card.querySelector('.form-guide');
        if (!guide) return;
        const expanded = toggle.getAttribute('aria-expanded') === 'true';
        toggle.setAttribute('aria-expanded', expanded ? 'false' : 'true');
        if (guide.hasAttribute('hidden')) {
            guide.removeAttribute('hidden');
        } else {
            guide.setAttribute('hidden', '');
        }
    });

    const blobs = document.querySelectorAll('.glow-blob');
    if (blobs.length && window.innerWidth > 768) {
        let rafId = null;
        let mx = 0, my = 0;
        document.addEventListener('mousemove', (e) => {
            const x = (e.clientX / window.innerWidth - 0.5) * 2;
            const y = (e.clientY / window.innerHeight - 0.5) * 2;
            mx = x;
            my = y;
            if (!rafId) {
                rafId = requestAnimationFrame(() => {
                    blobs.forEach((blob, i) => {
                        const factor = (i + 1) * 8;
                        const dx = mx * factor;
                        const dy = my * factor;
                        blob.style.transform = `translate(${dx}px, ${dy}px)`;
                    });
                    rafId = null;
                });
            }
        }, { passive: true });
    }

    if ('IntersectionObserver' in window) {
        const revealEls = document.querySelectorAll('.fh-reveal');
        if (revealEls.length) {
            const obs = new IntersectionObserver((entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('revealed');
                        obs.unobserve(entry.target);
                    }
                });
            }, { threshold: 0.15, rootMargin: '0px 0px -40px 0px' });
            revealEls.forEach((el) => obs.observe(el));
        }
    }

    const dropdown = document.querySelector('.nav-dropdown');
    if (dropdown) {
        const trigger = dropdown.querySelector('.nav-dropdown__trigger');
        const menu = dropdown.querySelector('.nav-dropdown__menu');
        if (trigger && menu) {
            trigger.addEventListener('click', (e) => {
                e.stopPropagation();
                const open = trigger.getAttribute('aria-expanded') === 'true';
                trigger.setAttribute('aria-expanded', open ? 'false' : 'true');
                menu.classList.toggle('is-open', !open);
            });
            document.addEventListener('click', (e) => {
                if (!dropdown.contains(e.target)) {
                    trigger.setAttribute('aria-expanded', 'false');
                    menu.classList.remove('is-open');
                }
            });
        }
    }
})();