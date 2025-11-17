// snippet.js
// Handles code highlighting, line numbers, auto-scroll, and file viewer for snippet detail page.

(() => {

  // ─────────────────────────────────────────────
  // 1. SIMPLE SYNTAX HIGHLIGHTER (lightweight)
  // ─────────────────────────────────────────────

  const highlightCode = (el, lang = "") => {
    let code = el.textContent;

    // Escape HTML
    code = code.replace(/[&<>]/g, c => ({ "&":"&amp;", "<":"&lt;", ">":"&gt;" }[c]));

    // Basic patterns
    const patterns = {
      keyword: /\b(class|def|return|if|else|elif|for|while|try|catch|finally|import|from|public|private|static|void|int|float|char|new)\b/g,
      string: /(".*?"|'.*?')/g,
      number: /\b(\d+)\b/g,
      comment: /(\/\/.*$|#.*$)/gm
    };

    // Apply styling
    code = code
      .replace(patterns.comment, `<span class="cmt">$1</span>`)
      .replace(patterns.string, `<span class="str">$1</span>`)
      .replace(patterns.keyword, `<span class="kw">$1</span>`)
      .replace(patterns.number, `<span class="num">$1</span>`);

    el.innerHTML = code;
  };


  // ─────────────────────────────────────────────
  // 2. ADD LINE NUMBERS
  // ─────────────────────────────────────────────
  const addLineNumbers = (codeEl) => {
    const code = codeEl.innerHTML.split("\n");
    const wrapper = document.createElement("div");
    wrapper.classList.add("code-wrapper");

    const gutter = document.createElement("div");
    gutter.classList.add("line-numbers");

    const content = document.createElement("pre");
    content.classList.add("code-content");
    content.innerHTML = codeEl.innerHTML;

    code.forEach((_, i) => {
      const num = document.createElement("span");
      num.textContent = i + 1;
      gutter.appendChild(num);
    });

    wrapper.appendChild(gutter);
    wrapper.appendChild(content);

    codeEl.replaceWith(wrapper);
  };


  // ─────────────────────────────────────────────
  // 3. FILE PREVIEW LOADER (Text-based files only)
  // ─────────────────────────────────────────────
  const loadFilePreview = () => {
    const viewer = document.getElementById("file-viewer");
    if (!viewer || !viewer.dataset.fileUrl) return;

    const url = viewer.dataset.fileUrl;

    fetch(url)
      .then(r => r.text())
      .then(txt => {
        viewer.innerHTML = `
          <h3>Uploaded File</h3>
          <pre><code id="file-code">${txt}</code></pre>
        `;
        const codeBlock = viewer.querySelector("#file-code");
        highlightCode(codeBlock);
      })
      .catch(() => {
        viewer.innerHTML = "<p>Unable to load file preview.</p>";
      });
  };


  // ─────────────────────────────────────────────
  // 4. AUTO SCROLL TO CODE ON PAGE LOAD
  // ─────────────────────────────────────────────
  const autoScrollToCode = () => {
    const target = document.querySelector(".code-wrapper, #snippet-code");
    if (!target) return;
    setTimeout(() => target.scrollIntoView({ behavior: "smooth", block: "center" }), 200);
  };


  // ─────────────────────────────────────────────
  // 5. INITIALIZE ON DOM READY
  // ─────────────────────────────────────────────
  document.addEventListener("DOMContentLoaded", () => {
    const snippet = document.getElementById("snippet-code");
    if (snippet) {
      highlightCode(snippet, snippet.dataset.lang);
      addLineNumbers(snippet);
    }

    loadFilePreview();
    autoScrollToCode();
  });

})();
