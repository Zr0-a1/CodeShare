// loading.js
// Simple full-screen loading overlay logic.
// HTML: <div id="loading-overlay"><div class="spinner"></div></div>
// CSS should place overlay fixed, centered spinner, etc.

(() => {
  const overlayId = 'loading-overlay';

  const hideOverlay = () => {
    const ov = document.getElementById(overlayId);
    if (!ov) return;
    ov.style.transition = 'opacity 450ms ease';
    ov.style.opacity = '0';
    setTimeout(() => { ov.remove(); }, 520);
  };

  // remove overlay when window fully loads (images included)
  window.addEventListener('load', hideOverlay);

  // fallback: remove after 6s to avoid forever-blocking in dev
  setTimeout(hideOverlay, 6000);

  // expose for manual control if needed
  window.__loading = {
    hide: hideOverlay,
    removeNow: () => {
      const ov = document.getElementById(overlayId);
      if (ov) ov.remove();
    }
  };
})();
