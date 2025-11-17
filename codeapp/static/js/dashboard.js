// dashboard.js
// Loads user's statistics: uploads, comments, reports, etc.

(() => {

  // ─────────────────────────────────────────
  // CONFIG
  // ─────────────────────────────────────────
  const API_URL = "/api/dashboard/";
  const REFRESH_INTERVAL = 30000; // 30s auto-refresh


  // ─────────────────────────────────────────
  // ANIMATED NUMBER COUNTER
  // ─────────────────────────────────────────
  const animateNumber = (el, value) => {
    let start = 0;
    const end = Number(value);
    if (isNaN(end)) return;

    const duration = 800;
    const step = Math.ceil(end / (duration / 16));

    const tick = () => {
      start += step;
      if (start >= end) {
        el.textContent = end;
      } else {
        el.textContent = start;
        requestAnimationFrame(tick);
      }
    };
    requestAnimationFrame(tick);
  };


  // ─────────────────────────────────────────
  // RENDER DASHBOARD WIDGETS
  // ─────────────────────────────────────────
  const updateDashboard = (data) => {
    const u = document.getElementById("db-total-uploads");
    const c = document.getElementById("db-total-comments");
    const r = document.getElementById("db-reports-pending");
    const list = document.getElementById("db-latest-list");

    if (u) animateNumber(u, data.uploads_count);
    if (c) animateNumber(c, data.comments_count);
    if (r) animateNumber(r, data.reports_pending);

    if (list) {
      list.innerHTML = "";
      data.latest_uploads.forEach(item => {
        const div = document.createElement("div");
        div.classList.add("dash-item");
        div.innerHTML = `
          <a href="/snippet/${item.id}/" class="dash-link">${item.title}</a>
        `;
        list.appendChild(div);
      });
    }
  };


  // ─────────────────────────────────────────
  // FETCH FROM SERVER
  // ─────────────────────────────────────────
  const loadDashboard = () => {
    fetch(API_URL)
      .then(r => r.json())
      .then(updateDashboard)
      .catch(err => console.error("Dashboard load error:", err));
  };


  // ─────────────────────────────────────────
  // INITIALIZE
  // ─────────────────────────────────────────
  document.addEventListener("DOMContentLoaded", () => {
    loadDashboard();
    setInterval(loadDashboard, REFRESH_INTERVAL);
  });

})();
