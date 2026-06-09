(function () {
    const menuToggle = document.getElementById('menuToggle');
    const mainNav = document.getElementById('mainNav');
    if (menuToggle && mainNav) {
        menuToggle.addEventListener('click', () => {
            const open = mainNav.classList.toggle('open');
            menuToggle.classList.toggle('active', open);
            menuToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
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
})();