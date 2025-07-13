// Injects the footer into the #footer-placeholder div
fetch("/Component/footer.html")
  .then((res) => res.text())
  .then((html) => {
    document.getElementById("footer-placeholder").innerHTML = html;
    // Optionally, re-initialize any required scripts for the footer here
  });
