// main.js
// Navbar toggles, search handling, copy/download protection, small helpers.

(() => {
  const body = document.body;
  const isAuthenticated = body.dataset.authenticated === 'true';

  // Mobile nav toggle (if you have one)
  document.addEventListener('click', (e) => {
    const t = e.target;
    // toggle button: data-nav-toggle
    if (t.matches('[data-nav-toggle]') || t.closest('[data-nav-toggle]')) {
      const nav = document.querySelector('.nav');
      if (nav) nav.classList.toggle('is-open');
    }
  });

  // highlight active nav link
  document.addEventListener('DOMContentLoaded', () => {
    const path = location.pathname.replace(/\/$/, '') || '/';
    document.querySelectorAll('nav a').forEach(a => {
      const href = a.getAttribute('href') || '';
      if (href === path || (href !== '/' && path.startsWith(href))) {
        a.classList.add('active');
      } else {
        a.classList.remove('active');
      }
    });
  });

  // Search form: submit to /?q=...
  const searchForms = document.querySelectorAll('form[data-search]');
  searchForms.forEach(form => {
    form.addEventListener('submit', (e) => {
      e.preventDefault();
      const q = (form.querySelector('input[name="q"]') || {}).value || '';
      // If not authenticated and you want search limited, you can redirect to login:
      // location.href = `/login/?next=${encodeURIComponent(location.pathname + '?q=' + q)}`;
      location.href = `/?q=${encodeURIComponent(q)}`;
    });
  });

  // Copy code button(s): <button data-copy data-snippet-id data-target="#codeblock">
  document.addEventListener('click', async (e) => {
    const btn = e.target.closest('[data-copy]');
    if (!btn) return;
    if (!isAuthenticated) {
      // Show login prompt modal or redirect
      alert('Please log in to copy code.');
      location.href = `/login/?next=${encodeURIComponent(location.pathname)}`;
      return;
    }

    const targetSelector = btn.dataset.target;
    const codeEl = targetSelector ? document.querySelector(targetSelector) : document.querySelector('.code-block');
    if (!codeEl) return;
    const text = codeEl.innerText || codeEl.textContent;
    try {
      await navigator.clipboard.writeText(text);
      btn.classList.add('copied');
      btn.innerText = 'Copied';
      setTimeout(()=> { btn.classList.remove('copied'); btn.innerText = btn.dataset.label || 'Copy'; }, 1500);
    } catch (err) {
      console.error('Copy failed', err);
      alert('Could not copy to clipboard.');
    }
  });

  // Download button protection: <a href="/download/123" data-download>
  document.addEventListener('click', (e) => {
    const dl = e.target.closest('[data-download]');
    if (!dl) return;
    if (!isAuthenticated) {
      e.preventDefault();
      alert('Please log in to download files.');
      location.href = `/login/?next=${encodeURIComponent(location.pathname)}`;
    }
    // If authenticated, allow normal navigation (server must enforce permission)
  });

  // small helper: set up confirm delete for admin (data-admin-delete)
  document.addEventListener('click', (e) => {
    const del = e.target.closest('[data-admin-delete]');
    if (!del) return;
    if (!confirm('Are you sure you want to delete this item?')) e.preventDefault();
  });

})();
