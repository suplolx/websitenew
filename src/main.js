// Project styles are loaded via link tag in HTML

// Navbar Scroll Logic
const header = document.getElementById('main-header');
const hero = document.querySelector('section.relative.h-screen');

const handleScroll = () => {
  if (!header) return;
  
  if (window.scrollY > 50) {
    header.classList.add('scrolled');
    header.classList.remove('nav-at-top');
  } else {
    header.classList.remove('scrolled');
    header.classList.add('nav-at-top');
  }
};

window.addEventListener('scroll', handleScroll);
handleScroll();

// Detect subpages (no hero banner) to tint the navbar
if (header && !hero) {
  header.classList.add('subpage-nav');
}

// Mobile Menu Toggle
const toggleMenu = (show) => {
  const mobileMenu = document.getElementById('mobile-menu');
  if (!mobileMenu) return;
  
  if (show) {
    mobileMenu.classList.add('active');
    document.body.style.overflow = 'hidden';
  } else {
    mobileMenu.classList.remove('active');
    document.body.style.overflow = '';
  }
};

document.addEventListener('click', (e) => {
  if (e.target.closest('.mobile-btn')) {
    toggleMenu(true);
  }
  if (e.target.closest('.close-menu') || e.target.closest('.mobile-nav-link')) {
    toggleMenu(false);
  }
});

// Scroll Reveal Animation (Intersection Observer)
const initScrollReveal = () => {
  const revealElements = document.querySelectorAll(
    '.group, section.py-32, section.py-20, section.py-16, .grid > div, .prose h2, .prose p, .bg-slate-50.p-8, .flex.items-start'
  );

  const observerOptions = {
    threshold: 0.05,
    rootMargin: '0px 0px -60px 0px'
  };

  const revealObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('reveal-visible');
        observer.unobserve(entry.target);
      }
    });
  }, observerOptions);

  revealElements.forEach(el => {
    el.classList.add('reveal-hidden');
    revealObserver.observe(el);
  });
};

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initScrollReveal);
} else {
  initScrollReveal();
}

