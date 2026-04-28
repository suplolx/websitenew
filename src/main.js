// Project styles are loaded via link tag in HTML

// Navbar Scroll Logic
const header = document.getElementById('main-header');
const hero = document.querySelector('section.relative.h-screen');

const handleScroll = () => {
  if (!header) return;
  
  if (window.scrollY > 50 || !hero) {
    header.classList.add('scrolled');
  } else {
    header.classList.remove('scrolled');
  }
};

window.addEventListener('scroll', handleScroll);
handleScroll();

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
