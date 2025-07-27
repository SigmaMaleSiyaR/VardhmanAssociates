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
      return "<p>Content not available. Please check back later.</p>";
    }
  } catch (error) {
    console.error("Error fetching service content:", error);
    return "<p>Error loading content. Please try again later.</p>";
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
  container.innerHTML =
    '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div><p class="mt-2">Loading content...</p></div>';

  try {
    const content = await fetchServiceContent(serviceType, serviceTitle);
    container.innerHTML = content;
  } catch (error) {
    console.error("Error displaying service content:", error);
    container.innerHTML =
      '<div class="alert alert-danger">Error loading content. Please try again later.</div>';
  }
}

// Export the function for use in other files
export { fetchServiceContent, displayServiceContent };
