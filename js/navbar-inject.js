// Injects the navbar into the #navbar-placeholder div
fetch('/Services/Ca/navbar.html')
  .then(res => res.text())
  .then(html => {
    document.getElementById('navbar-placeholder').innerHTML = html;
    // Re-initialize Bootstrap dropdowns if needed
    if (window.bootstrap) {
      var dropdownElementList = [].slice.call(document.querySelectorAll('.dropdown-toggle'));
      dropdownElementList.map(function (dropdownToggleEl) {
        return new bootstrap.Dropdown(dropdownToggleEl);
      });
    }
  }); 