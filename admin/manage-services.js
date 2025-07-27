import { db } from "./firebase-config.js";
import {
  collection,
  getDocs,
  query,
  where,
} from "https://www.gstatic.com/firebasejs/11.9.0/firebase-firestore.js";

const predefinedTitles = {
  CA: [
    "Start A Business",
    "Business Registration & Licence",
    "Income Tax",
    "GST Services",
    "TDS Services",
    "ESI & PF Services",
    "Income Tax Notice & Appeal",
    "Accounting & Auditing",
    "Society and NGO",
    "CMA Data & Project Report",
    "Loans & Project Finance",
  ],
  CS: [
    "Annual Compliances",
    "Corporate & Financial Restructuring",
    "Due Diligence",
    "Company Incorporation & Amendment",
    "Company Strike off & Closer",
    "Winding Up & Dissolution",
    "Secretarial Audit",
    "Insolvency and Bankruptcy Matters",
    "XBRL Filing",
    "NCLT Appeal",
    "Appointment & Resignation",
    "RBI & FEMA Overseas Law Compliance",
    "Minutes & Resolutions",
    "XML Data Conversion",
    "Share Certificate & Transfer",
  ],
  Advocate: [
    "Civil Law",
    "Banking & Finance Law",
    "Legal Advisory",
    "Consumer Law & Protection",
    "Corporate Law & Advisory",
    "Family Law",
    "Deed Making & Drafting",
    "Debt Recovery & Suit",
    "Labour & Employment Law",
    "NIA Matter",
    "Property Valuation Services",
    "Real Estate & Regulatory Act (RERA)",
    "Appeal",
    "SARFAESI Law",
  ],
};

let currentType = "CA";
const serviceDropdown = document.getElementById("serviceDropdown");

function setType(type) {
  currentType = type;
  // Highlight the selected button
  document.getElementById("btn-ca").classList.remove("active");
  document.getElementById("btn-cs").classList.remove("active");
  document.getElementById("btn-advocate").classList.remove("active");
  document.getElementById(`btn-${type.toLowerCase()}`).classList.add("active");
  // Populate dropdown with hardcoded titles
  serviceDropdown.innerHTML =
    '<option value="">-- Select Service to Edit --</option>';
  if (predefinedTitles[type]) {
    predefinedTitles[type].forEach((title) => {
      serviceDropdown.innerHTML += `<option value="${title}">${title}</option>`;
    });
  }
  // Optionally, you can still load the list of services for display
  loadServices();
}

document.getElementById("btn-ca").onclick = () => setType("CA");
document.getElementById("btn-cs").onclick = () => setType("CS");
document.getElementById("btn-advocate").onclick = () => setType("Advocate");

serviceDropdown.onchange = function () {
  const selectedTitle = this.value;
  const editContentBtn = document.getElementById("editContentBtn");
  const messageDiv = document.getElementById("message");

  if (!selectedTitle || selectedTitle.trim() === "") {
    editContentBtn.style.display = "none";
    messageDiv.innerHTML = "";
    return;
  }

  // Show the edit button
  editContentBtn.style.display = "inline-block";
  editContentBtn.onclick = function () {
    if (
      currentType &&
      selectedTitle &&
      currentType.trim() !== "" &&
      selectedTitle.trim() !== ""
    ) {
      window.location.href = `edit-service.html?type=${encodeURIComponent(
        currentType
      )}&title=${encodeURIComponent(selectedTitle)}`;
    } else {
      messageDiv.innerHTML =
        '<div class="alert alert-danger">Error: Please select a valid service type and title.</div>';
    }
  };
};

document.getElementById("editContentBtn").style.display = "none";

async function loadServices() {
  // Optionally, show a list of all services for the selected type
  const existingServicesDiv = document.getElementById("existingServices");
  existingServicesDiv.innerHTML = "<b>Loading...</b>";
  const q = query(collection(db, "services"), where("type", "==", currentType));
  const querySnapshot = await getDocs(q);
  if (querySnapshot.empty) {
    existingServicesDiv.innerHTML = `<i>No ${currentType} services found.</i>`;
    return;
  }
  let html = `<h3>${currentType} Services</h3><ul class='list-group'>`;
  querySnapshot.forEach((docSnap) => {
    const data = docSnap.data();
    html += `<li class='list-group-item'><b>${data.title}</b>: ${data.content}</li>`;
  });
  html += "</ul>";
  existingServicesDiv.innerHTML = html;
}

// Initial load
setType(currentType);
