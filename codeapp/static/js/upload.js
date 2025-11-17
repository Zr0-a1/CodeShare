// upload.js
// Handles upload form preview and client-side validation.
// Expects input[name="file"] and an element with id="file-preview" to show file name/size.
// Uses same 5MB limit set in settings: DATA_UPLOAD_MAX_MEMORY_SIZE = 5 * 1024 * 1024

(() => {
  const MAX_BYTES = 5 * 1024 * 1024; // 5 MB
  const allowedExt = ['.py','.java','.cpp','.c','.js','.html','.css','.dart','.txt','.zip'];

  const getExt = (name) => {
    const i = name.lastIndexOf('.');
    return i >= 0 ? name.substr(i).toLowerCase() : '';
  };

  document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.querySelector('input[type="file"][name="file"]');
    const preview = document.getElementById('file-preview');
    const form = document.querySelector('form[data-upload]');
    if (!fileInput || !form) return;

    fileInput.addEventListener('change', (e) => {
      const f = fileInput.files[0];
      if (!f) {
        if (preview) preview.innerHTML = '';
        return;
      }
      const ext = getExt(f.name);
      if (!allowedExt.includes(ext)) {
        alert('File type not allowed. Allowed: ' + allowedExt.join(', '));
        fileInput.value = '';
        if (preview) preview.innerHTML = '';
        return;
      }
      if (f.size > MAX_BYTES) {
        alert('File is too large. Maximum allowed size is 5 MB.');
        fileInput.value = '';
        if (preview) preview.innerHTML = '';
        return;
      }
      if (preview) {
        preview.innerHTML = `<strong>${f.name}</strong> — ${(f.size/1024).toFixed(1)} KB`;
      }
    });

    // prevent multiple submits
    form.addEventListener('submit', (e) => {
      const submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.dataset.orig = submitBtn.innerText;
        submitBtn.innerText = 'Uploading...';
      }
    });
  });
})();
