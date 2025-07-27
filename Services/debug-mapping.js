// Debug script to test service mapping
// Add this to any service page to see what's being detected

import {
  getServiceTypeFromPath,
  getServiceTitleFromPage,
} from "./service-content-loader.js";

function debugServiceMapping() {
  console.log("🔍 Debugging Service Mapping...");
  console.log("=" * 50);

  const serviceType = getServiceTypeFromPath();
  const serviceTitle = getServiceTitleFromPage();

  console.log("📍 Current Page Info:");
  console.log("- URL:", window.location.href);
  console.log("- Path:", window.location.pathname);
  console.log("- Title:", document.title);

  console.log("\n🎯 Detected Values:");
  console.log("- Service Type:", serviceType);
  console.log("- Service Title:", serviceTitle);

  console.log("\n🔍 Firebase Query:");
  console.log(`Collection: "services"`);
  console.log(`Where: type == "${serviceType}"`);
  console.log(`Where: title == "${serviceTitle}"`);

  console.log("\n📋 Expected Firebase Document:");
  console.log(
    JSON.stringify(
      {
        type: serviceType,
        title: serviceTitle,
        content: "<h2>Your content here</h2>",
      },
      null,
      2
    )
  );

  console.log("\n💡 Admin Panel Mapping:");
  console.log("- Go to /admin/manage-services.html");
  console.log("- Select service type:", serviceType);
  console.log("- Choose service:", serviceTitle);
  console.log("- Add content and save");

  console.log("=" * 50);
}

// Run debug when page loads
document.addEventListener("DOMContentLoaded", debugServiceMapping);

// Also make it available globally for manual testing
window.debugServiceMapping = debugServiceMapping;
