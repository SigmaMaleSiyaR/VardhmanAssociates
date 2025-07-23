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
