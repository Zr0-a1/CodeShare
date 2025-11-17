// animations.js
// Handles hover animations, button click ripple, small UI transitions.

(() => {
  const addHoverLift = (selector, lift = 6) => {
    document.querySelectorAll(selector).forEach(el => {
      el.style.transition = 'transform 180ms ease, box-shadow 180ms ease';
      el.addEventListener('mouseenter', () => {
        el.style.transform = `translateY(-${lift}px)`;
        el.style.boxShadow = '0 10px 25px rgba(0,0,0,0.08)';
      });
      el.addEventListener('mouseleave', () => {
        el.style.transform = '';
        el.style.boxShadow = '';
      });
    });
  };

  // ripple effect for buttons
  const addButtonRipple = (selector) => {
    document.querySelectorAll(selector).forEach(btn => {
      btn.style.position = 'relative';
      btn.style.overflow = 'hidden';
      btn.addEventListener('click', (e) => {
        const rect = btn.getBoundingClientRect();
        const circle = document.createElement('span');
        const size = Math.max(rect.width, rect.height) * 1.4;
        circle.style.width = circle.style.height = `${size}px`;
        circle.style.position = 'absolute';
        circle.style.borderRadius = '50%';
        circle.style.background = 'rgba(255,255,255,0.15)';
        circle.style.left = `${e.clientX - rect.left - size/2}px`;
        circle.style.top = `${e.clientY - rect.top - size/2}px`;
        circle.style.pointerEvents = 'none';
        circle.style.transform = 'scale(0)';
        circle.style.transition = 'transform 400ms ease, opacity 400ms ease';
        btn.appendChild(circle);
        requestAnimationFrame(() => circle.style.transform = 'scale(1)');
        setTimeout(() => {
          circle.style.opacity = '0';
          setTimeout(()=> circle.remove(), 450);
        }, 300);
      });
    });
  };

  // small fade-in for elements with .fade-in
  const fadeInOnVisible = (selector, rootMargin = '0px 0px -10% 0px') => {
    const items = document.querySelectorAll(selector);
    if (!items.length) return;
    const io = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.transition = 'opacity 500ms ease, transform 500ms ease';
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.06, rootMargin });
    items.forEach(it => {
      it.style.opacity = '0';
      it.style.transform = 'translateY(12px)';
      io.observe(it);
    });
  };

  // init on DOM ready
  document.addEventListener('DOMContentLoaded', () => {
    addHoverLift('.card, .snippet, .project-card', 8);
    addButtonRipple('button, .btn, .nav-btn');
    fadeInOnVisible('.fade-in, .card, .project-card');
  });

})();
