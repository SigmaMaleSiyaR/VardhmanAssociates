import { db } from "./firebase-config.js";
import {
  collection,
  addDoc,
  getDocs,
  query,
  where,
  updateDoc,
  doc,
} from "https://www.gstatic.com/firebasejs/11.9.0/firebase-firestore.js";
import {
  IMAGEKIT_PUBLIC_KEY,
  IMAGEKIT_AUTH_ENDPOINT,
  IMAGEKIT_CONTENT_FOLDER,
} from "./imagekit-config.js";

function getQueryParam(name) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(name);
}

const type = getQueryParam("type");
const title = getQueryParam("title");

document.getElementById("serviceType").value = type || "";
document.getElementById("serviceTitle").value = title || "";

const messageDiv = document.getElementById("message");

// Show warning if accessed without proper parameters
if (!type || !title || type.trim() === "" || title.trim() === "") {
  messageDiv.innerHTML =
    '<div class="alert alert-warning"><strong>Warning:</strong> No service selected. Please go back to <a href="manage-services.html" class="alert-link">Manage Services</a> and select a service to edit.</div>';
}

// Register quill-better-table module only
if (window.Quill && window.quillBetterTable) {
  Quill.register(
    {
      "modules/better-table": window.quillBetterTable,
    },
    true
  );
}

// Upload to ImageKit (same logic as add-blog, but use CONTENT_FOLDER)
async function uploadImageToImageKit(file) {
  return new Promise((resolve, reject) => {
    fetch(IMAGEKIT_AUTH_ENDPOINT)
      .then((res) => res.json())
      .then((authData) => {
        const formData = new FormData();
        formData.append("file", file);
        formData.append("fileName", `${Date.now()}_${file.name}`);
        formData.append("token", authData.token);
        formData.append("signature", authData.signature);
        formData.append("expire", authData.expire);
        formData.append("publicKey", IMAGEKIT_PUBLIC_KEY);
        formData.append("folder", IMAGEKIT_CONTENT_FOLDER);
        fetch("https://upload.imagekit.io/api/v1/files/upload", {
          method: "POST",
          body: formData,
        })
          .then((res) => res.json())
          .then(resolve)
          .catch((err) => reject(new Error(err.message || "Upload failed")));
      })
      .catch(() => reject(new Error("Failed to get authentication token")));
  });
}

// Custom handler for image and video
function mediaHandler(type) {
  return function () {
    const input = document.createElement("input");
    input.setAttribute("type", "file");
    input.setAttribute("accept", type === "image" ? "image/*" : "video/*");
    input.click();
    input.onchange = async () => {
      const file = input.files[0];
      if (file) {
        const range = quill.getSelection(true);
        try {
          const imageKitRes = await uploadImageToImageKit(file);
          const url = imageKitRes.url;
          if (type === "image") {
            quill.insertEmbed(range.index, "image", url);
          } else if (type === "video") {
            quill.insertEmbed(range.index, "video", url);
          }
          quill.setSelection(range.index + 1, 0);
        } catch (err) {
          alert("Upload failed: " + err.message);
        }
      }
    };
  };
}

// Remove better-table module and toolbar button
const quill = new Quill("#quillEditor", {
  theme: "snow",
  modules: {
    toolbar: {
      container: [
        [{ header: [1, 2, 3, false] }],
        ["bold", "italic", "underline", "strike"],
        [{ color: [] }, { background: [] }],
        [{ list: "ordered" }, { list: "bullet" }],
        [{ align: [] }],
        ["blockquote", "code-block"],
        ["link", "image", "video"],
        ["clean"],
      ],
      handlers: {
        image: mediaHandler("image"),
        video: mediaHandler("video"),
      },
    },
  },
});

// Load content from Firestore
async function loadContent() {
  if (!type || !title) return;
  const q = query(
    collection(db, "services"),
    where("type", "==", type),
    where("title", "==", title)
  );
  const querySnapshot = await getDocs(q);
  if (!querySnapshot.empty) {
    const data = querySnapshot.docs[0].data();
    quill.root.innerHTML = data.content || "";
  } else {
    quill.root.innerHTML = "";
  }
}

loadContent();

document.getElementById("editServiceForm").onsubmit = async function (e) {
  e.preventDefault();

  // Validate service type and title
  if (!type || !title || type.trim() === "" || title.trim() === "") {
    messageDiv.innerHTML =
      '<div class="alert alert-danger">Error: Service type and title are required. Please select a valid service from the manage services page.</div>';
    return;
  }

  const content = quill.root.innerHTML.trim();
  document.getElementById("serviceContent").value = content;

  // Validate content
  if (!content) {
    messageDiv.innerHTML =
      '<div class="alert alert-warning">Warning: Service content cannot be empty. Please add some content before saving.</div>';
    return;
  }

  try {
    // Check if a service with this type and title exists
    const q = query(
      collection(db, "services"),
      where("type", "==", type),
      where("title", "==", title)
    );
    const querySnapshot = await getDocs(q);
    if (!querySnapshot.empty) {
      // Update existing
      const docRef = querySnapshot.docs[0].ref;
      await updateDoc(docRef, { content });
      messageDiv.innerHTML =
        '<div class="alert alert-success">Content updated successfully!</div>';
    } else {
      // Add new
      await addDoc(collection(db, "services"), {
        type,
        title,
        content,
      });
      messageDiv.innerHTML =
        '<div class="alert alert-success">Content added successfully!</div>';
    }
  } catch (err) {
    messageDiv.innerHTML = `<div class="alert alert-danger">Error: ${err.message}</div>`;
  }
};
