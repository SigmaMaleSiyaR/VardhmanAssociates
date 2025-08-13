fetch("/Component/navbar.html")
  .then((res) => res.text())
  .then((html) => {
    const placeholder = document.getElementById("navbar-placeholder");
    placeholder.innerHTML = html;

    // ✅ Force reflow after DOM injection (to allow CSS/animations to take effect)
    setTimeout(() => {
      // placeholder.style.height = `100px`;
    }, 100); // Give time for animations to render

    // ✅ Re-initialize Bootstrap dropdowns
    if (window.bootstrap) {
      const dropdowns = [].slice.call(
        document.querySelectorAll(".dropdown-toggle")
      );
      dropdowns.map((el) => new bootstrap.Dropdown(el));
    }

    // ✅ Activate link via global variable (like contact, about, etc.)
    const activePage = window.activepage?.toLowerCase();
    console.log("Active Page:", activePage);

    if (activePage) {
      document
        .querySelectorAll("#navbar-placeholder a.nav-link")
        .forEach((link) => {
          const text = link.textContent.trim().toLowerCase();
          if (text === activePage) {
            link.classList.add("active");
          } else {
            link.classList.remove("active");
          }
        });
    }

    // ✅ Special logic for Services dropdown
    const currentPath = window.location.pathname.toLowerCase();
    if (
      currentPath.includes("/services/ca/") ||
      currentPath.includes("/services/cs/") ||
      currentPath.includes("/services/advocate/")
    ) {
      const dropdownLink = document.querySelector(
        "#navbar-placeholder .nav-link.dropdown-toggle"
      );
      if (dropdownLink) {
        dropdownLink.classList.add("active");
      }
    }
  });

// Inject 100vh sidebar behavior for all Services pages
try {
  const path = window.location.pathname.toLowerCase();
  if (
    path.includes("/services/ca/") ||
    path.includes("/services/cs/") ||
    path.includes("/services/advocate/")
  ) {
    const style = document.createElement("style");
    style.textContent = `
        @media (min-width: 992px) {
          #sidebar {
            max-height: calc(100vh - 100px);
            overflow: hidden;
            display: flex;
            flex-direction: column;
          }
          #sidebar ul {
            flex: 1 1 auto;
            overflow-y: auto;
            margin: 0;
            padding-left: 1rem;
          }
          #sidebar li { margin-bottom: 6px; }
          #sidebar a { padding: 6px 0; min-height: 36px; }
          #sidebar a p { margin: 0; }
        }
      `;
    document.head.appendChild(style);
  }
} catch (e) {
  console.warn("Sidebar 100vh style injection failed:", e);
}
