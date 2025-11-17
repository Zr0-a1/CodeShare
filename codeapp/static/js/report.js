// report.js
// Send a "report faulty code" action via fetch to your backend API.
// Expects forms/buttons with data-report attributes or a report form with data-report-form

(() => {
  // helper to read CSRF token from cookie (Django default)
  const getCookie = (name) => {
    const v = document.cookie.split(';').map(c => c.trim()).filter(c => c.startsWith(name + '='));
    if (!v.length) return null;
    return decodeURIComponent(v[0].split('=')[1]);
  };

  const csrf = getCookie('csrftoken');

  // Attach to buttons with data-report: <button data-report data-snippet="123">Report</button>
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-report]');
    if (!btn) return;
    const snippetId = btn.dataset.snippet;
    if (!snippetId) {
      alert('Snippet id missing.');
      return;
    }
    const reason = prompt('Describe the problem with this snippet (why it fails):', '');
    if (!reason) return;
    btn.disabled = true;
    fetch('/api/report/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf || ''
      },
      body: JSON.stringify({ snippet_id: snippetId, reason })
    }).then(r => r.json())
      .then(data => {
        if (data && data.ok) {
          alert('Report submitted. Admin will review it.');
        } else {
          alert('Could not submit report. Try again.');
        }
      })
      .catch(err => {
        console.error(err);
        alert('Network error while reporting.');
      })
      .finally(() => btn.disabled = false);
  });

  // Optionally handle a dedicated report form
  document.addEventListener('submit', (e) => {
    const form = e.target.closest('form[data-report-form]');
    if (!form) return;
    e.preventDefault();
    const snippetId = form.querySelector('input[name="snippet_id"]').value;
    const reason = (form.querySelector('textarea[name="reason"]').value || '').trim();
    if (!reason) return alert('Please provide a reason.');
    const submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) submitBtn.disabled = true;
    fetch('/api/report/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': csrf || ''
      },
      body: JSON.stringify({ snippet_id: snippetId, reason })
    }).then(r => r.json())
      .then(data => {
        if (data && data.ok) {
          alert('Report submitted.');
          form.reset();
        } else {
          alert('Failed to submit report.');
        }
      })
      .catch(() => alert('Network error.'))
      .finally(() => { if (submitBtn) submitBtn.disabled = false; });
  });

})();
