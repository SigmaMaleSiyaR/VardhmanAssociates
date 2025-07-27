import { db } from "./firebase-config.js";
import {
  collection,
  getDocs,
  query,
  where,
} from "https://www.gstatic.com/firebasejs/11.9.0/firebase-firestore.js";

// Function to fetch service content from Firebase
async function fetchServiceContent(serviceType, serviceTitle) {
  try {
    const q = query(
      collection(db, "services"),
      where("type", "==", serviceType),
      where("title", "==", serviceTitle)
    );

    const querySnapshot = await getDocs(q);

    if (!querySnapshot.empty) {
      const data = querySnapshot.docs[0].data();
      return data.content || "";
    } else {
      return "<div class='alert alert-info'><h4>Content Coming Soon</h4><p>We're currently preparing the content for this service. Please check back later or contact us for more information.</p></div>";
    }
  } catch (error) {
    console.error("Error fetching service content:", error);
    return "<div class='alert alert-danger'><h4>Error Loading Content</h4><p>We're experiencing technical difficulties. Please try again later or contact us for assistance.</p></div>";
  }
}

// Function to display service content
async function displayServiceContent(serviceType, serviceTitle, containerId) {
  const container = document.getElementById(containerId);

  if (!container) {
    console.error(`Container with id '${containerId}' not found`);
    return;
  }

  // Show loading state
  container.innerHTML = `
    <div class="text-center py-5">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
      <p class="mt-3 text-muted">Loading service content...</p>
    </div>
  `;

  try {
    const content = await fetchServiceContent(serviceType, serviceTitle);
    container.innerHTML = content;

    // Add some spacing at the bottom
    container.innerHTML += '<div style="margin-bottom: 2rem;"></div>';
  } catch (error) {
    console.error("Error displaying service content:", error);
    container.innerHTML = `
      <div class="alert alert-danger">
        <h4>Error Loading Content</h4>
        <p>We're experiencing technical difficulties. Please try again later or contact us for assistance.</p>
        <button class="btn btn-outline-danger btn-sm" onclick="location.reload()">Retry</button>
      </div>
    `;
  }
}

// Function to get service type from URL path
function getServiceTypeFromPath() {
  const path = window.location.pathname;
  if (path.includes("/Ca/")) return "CA";
  if (path.includes("/Cs/")) return "CS";
  if (path.includes("/Advocate/")) return "Advocate";
  return null;
}

// Function to get service title from page title or URL
function getServiceTitleFromPage() {
  // Try to get from page title first
  const pageTitle = document.title;
  if (pageTitle && pageTitle !== "") {
    // Extract service name from title (remove "- CA Services" or similar)
    const serviceName = pageTitle
      .replace(/\s*-\s*(CA|CS|Advocate)\s*Services.*$/, "")
      .trim();
    if (serviceName) return serviceName;
  }

  // Fallback: try to get from URL path
  const path = window.location.pathname;
  const filename = path.split("/").pop();
  if (filename && filename !== "") {
    // Remove .html extension and decode URL
    const serviceName = decodeURIComponent(filename.replace(".html", ""));
    return serviceName;
  }

  return null;
}

// Auto-load content based on current page
function autoLoadServiceContent() {
  const serviceType = getServiceTypeFromPath();
  const serviceTitle = getServiceTitleFromPage();

  if (serviceType && serviceTitle) {
    displayServiceContent(serviceType, serviceTitle, "service-content");
  } else {
    console.error(
      "Could not determine service type or title from current page"
    );
    const container = document.getElementById("service-content");
    if (container) {
      container.innerHTML = `
        <div class="alert alert-warning">
          <h4>Service Not Found</h4>
          <p>Unable to determine which service to load. Please contact support.</p>
        </div>
      `;
    }
  }
}

// Export functions for manual use
export { fetchServiceContent, displayServiceContent, autoLoadServiceContent };
