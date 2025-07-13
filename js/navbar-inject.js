fetch("/Services/navbar.html")
  .then((res) => res.text())
  .then((html) => {
    const placeholder = document.getElementById("navbar-placeholder");
    placeholder.innerHTML = html;

    // ✅ Force reflow after DOM injection (to allow CSS/animations to take effect)
    setTimeout(() => {
      placeholder.style.height = `100px`;
    }, 100); // Give time for animations to render

    // ✅ Re-initialize Bootstrap dropdowns
    if (window.bootstrap) {
      const dropdowns = [].slice.call(
        document.querySelectorAll(".dropdown-toggle")
      );
      dropdowns.map((el) => new bootstrap.Dropdown(el));
    }
  });
