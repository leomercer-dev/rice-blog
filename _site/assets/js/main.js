/* ╔══════════════════════════════════════════╗
   ║  Rice Blog — Main JavaScript             ║
   ║  Pure vanilla. Zero dependencies.        ║
   ╚══════════════════════════════════════════╝ */

(function() {
    'use strict';
    
    // ── Mobile Menu Toggle ────────────────────
    const menuToggle = document.querySelector('.menu-toggle');
    const navLinks = document.querySelector('.navbar-links');
    
    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', function() {
            const isOpen = navLinks.style.display === 'flex';
            navLinks.style.display = isOpen ? 'none' : 'flex';
            navLinks.style.flexDirection = 'column';
            navLinks.style.position = 'absolute';
            navLinks.style.top = '56px';
            navLinks.style.left = '0';
            navLinks.style.right = '0';
            navLinks.style.background = 'rgba(17, 17, 27, 0.95)';
            navLinks.style.padding = '1rem 2rem';
            navLinks.style.borderBottom = '1px solid var(--surface0)';
            navLinks.style.gap = '0.8rem';
        });
        
        // Close on resize
        window.addEventListener('resize', function() {
            if (window.innerWidth > 640) {
                navLinks.style.display = '';
                navLinks.style.flexDirection = '';
                navLinks.style.position = '';
                navLinks.style.top = '';
                navLinks.style.left = '';
                navLinks.style.right = '';
                navLinks.style.background = '';
                navLinks.style.padding = '';
                navLinks.style.borderBottom = '';
                navLinks.style.gap = '';
            }
        });
    }
    
    // ── Lightbox for Gallery Images ───────────
    const galleryImages = document.querySelectorAll('.rice-gallery img');
    const lightbox = document.getElementById('lightbox');
    
    galleryImages.forEach(function(img) {
        img.addEventListener('click', function() {
            if (lightbox) {
                lightbox.querySelector('img').src = this.src;
                lightbox.classList.add('active');
            }
        });
    });
    
    if (lightbox) {
        lightbox.addEventListener('click', function() {
            this.classList.remove('active');
        });
        
        // Close on Escape key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                lightbox.classList.remove('active');
            }
        });
    }
    
    // ── Smooth Scroll for Anchor Links ────────
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
    
    // ── Back to Top Button ────────────────────
    const backToTop = document.getElementById('back-to-top');
    if (backToTop) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 400) {
                backToTop.style.opacity = '1';
                backToTop.style.pointerEvents = 'auto';
            } else {
                backToTop.style.opacity = '0';
                backToTop.style.pointerEvents = 'none';
            }
        }, { passive: true });
        
        backToTop.addEventListener('click', function() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
    
    // ── Lazy Loading for Images ───────────────
    if ('IntersectionObserver' in window) {
        const lazyImages = document.querySelectorAll('img[data-src]');
        const imageObserver = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src || '';
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        lazyImages.forEach(function(img) {
            imageObserver.observe(img);
        });
    }
    
    // ── Dark/Light Mode Toggle ────────────────
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {
        // Check saved preference
        const saved = localStorage.getItem('theme') || 'dark';
        document.documentElement.classList.toggle('light', saved === 'light');
        
        themeToggle.addEventListener('click', function() {
            const isLight = document.documentElement.classList.toggle('light');
            localStorage.setItem('theme', isLight ? 'light' : 'dark');
        });
    }
    
    // ── Active Nav Link Highlighting ──────────
    const currentPath = window.location.pathname;
    document.querySelectorAll('.navbar-links a').forEach(function(link) {
        const href = link.getAttribute('href');
        if (currentPath === href || (href !== '/' && currentPath.startsWith(href))) {
            link.classList.add('active');
        }
    });
    
})();
