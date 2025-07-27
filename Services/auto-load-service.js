// Auto-load service content script
// Include this script in any service page to automatically load content from Firebase

import { autoLoadServiceContent } from "./service-content-loader.js";

// Auto-load content when DOM is ready
document.addEventListener("DOMContentLoaded", function () {
  autoLoadServiceContent();
});
