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
  if (e.target.closest('.close-menu') || (e.target.closest('.mobile-nav-link') && !e.target.closest('.mobile-dropdown-btn'))) {
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

// Intake Form Mailto Handler
const intakeForm = document.getElementById('intake-form');
if (intakeForm) {
  intakeForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const name = document.getElementById('name')?.value || '';
    const organization = document.getElementById('organization')?.value || '';
    const email = document.getElementById('email')?.value || '';
    const phone = document.getElementById('phone')?.value || '';
    const service = document.getElementById('service')?.value || '';
    const message = document.getElementById('message')?.value || '';

    // Format the email body
    const emailSubject = `Aanvraag Intake Verwijzer - ${name}`;
    const emailBody = `Beste Kr8tig,

Hierbij ontvangt u een aanvraag voor een intake:

Naam verwijzer: ${name}
Organisatie / Gemeente: ${organization}
E-mailadres: ${email}
Telefoonnummer: ${phone}
Gewenste dienst(en): ${service}

Korte toelichting:
${message}

Met vriendelijke groet,
${name}`;

    // Create mailto link
    const mailtoLink = `mailto:info@kr8tig.nl?subject=${encodeURIComponent(emailSubject)}&body=${encodeURIComponent(emailBody)}`;
    
    // Open default mail client
    window.location.href = mailtoLink;
  });
}

// Mobile Accordion Dropdown Toggle
document.addEventListener('click', (e) => {
  const dropdownButton = e.target.closest('.mobile-dropdown-btn');
  if (dropdownButton) {
    const parent = dropdownButton.closest('.mobile-dropdown');
    const content = parent?.querySelector('.mobile-dropdown-content');
    const arrow = parent?.querySelector('.mobile-arrow');
    if (content && arrow) {
      if (content.classList.contains('hidden')) {
        content.classList.remove('hidden');
        content.classList.add('flex');
        arrow.classList.add('rotate-180');
      } else {
        content.classList.add('hidden');
        content.classList.remove('flex');
        arrow.classList.remove('rotate-180');
      }
    }
  }
});

// Vacancy Accordion Toggle
document.addEventListener('click', (e) => {
  const header = e.target.closest('.vacancy-header');
  if (header) {
    const card = header.closest('.vacancy-card');
    const details = card?.querySelector('.vacancy-details');
    const arrow = card?.querySelector('.vacancy-arrow');
    if (details && arrow) {
      if (details.classList.contains('hidden')) {
        details.classList.remove('hidden');
        arrow.classList.add('rotate-180');
        card.classList.add('border-primary/30');
      } else {
        details.classList.add('hidden');
        arrow.classList.remove('rotate-180');
        card.classList.remove('border-primary/30');
      }
    }
  }
});

