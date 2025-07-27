import { auth, db } from "./firebase-config.js";
import {
  onAuthStateChanged,
  signOut,
  createUserWithEmailAndPassword,
  deleteUser,
} from "https://www.gstatic.com/firebasejs/11.9.0/firebase-auth.js";
import {
  collection,
  doc,
  setDoc,
  getDocs,
  deleteDoc,
  query,
  where,
  serverTimestamp,
} from "https://www.gstatic.com/firebasejs/11.9.0/firebase-firestore.js";

// DOM elements
const currentUserElement = document.getElementById("currentUser");
const logoutBtn = document.getElementById("logoutBtn");
const adminList = document.getElementById("adminList");
const messageContainer = document.getElementById("messageContainer");
const addAdminForm = document.getElementById("addAdminForm");
const deleteAdminModal = document.getElementById("deleteAdminModal");
const deleteAdminEmail = document.getElementById("deleteAdminEmail");
const confirmDeleteBtn = document.getElementById("confirmDeleteBtn");

let currentUser = null;
let adminToDelete = null;

// Check authentication status
onAuthStateChanged(auth, async (user) => {
  if (user) {
    currentUser = user;
    currentUserElement.innerHTML = `<i class="fas fa-user"></i> ${user.email}`;

    // Check if user is super admin
    const isSuperAdmin = await checkSuperAdminStatus(user.uid);
    if (!isSuperAdmin) {
      showMessage(
        "Access denied. Only super admins can manage admin accounts.",
        "danger"
      );
      setTimeout(() => {
        window.location.href = "/admin/manage-blogs.html";
      }, 2000);
      return;
    }

    // Load admin list
    loadAdminList();
  } else {
    // Redirect to login if not authenticated
    window.location.href = "/admin/index.html";
  }
});

// Logout functionality
logoutBtn.addEventListener("click", async (e) => {
  e.preventDefault();
  try {
    await signOut(auth);
    window.location.href = "/admin/index.html";
  } catch (error) {
    showMessage("Error logging out: " + error.message, "danger");
  }
});

// Check if user is super admin
async function checkSuperAdminStatus(uid) {
  try {
    const adminDoc = await getDocs(
      query(collection(db, "admins"), where("uid", "==", uid))
    );

    if (!adminDoc.empty) {
      const adminData = adminDoc.docs[0].data();
      return adminData.role === "super_admin";
    }

    // If no admin record found, check if this is the first user (make them super admin)
    const allAdmins = await getDocs(collection(db, "admins"));
    if (allAdmins.empty) {
      // First user becomes super admin
      await setDoc(doc(db, "admins", uid), {
        uid: uid,
        email: currentUser.email,
        name: currentUser.email.split("@")[0], // Use email prefix as name
        role: "super_admin",
        createdAt: serverTimestamp(),
      });
      return true;
    }

    return false;
  } catch (error) {
    console.error("Error checking admin status:", error);
    return false;
  }
}

// Load admin list
async function loadAdminList() {
  try {
    adminList.innerHTML = `
      <div class="text-center">
        <div class="spinner-border" role="status">
          <span class="visually-hidden">Loading...</span>
        </div>
        <p class="mt-2">Loading admin accounts...</p>
      </div>
    `;

    const adminSnapshot = await getDocs(collection(db, "admins"));

    if (adminSnapshot.empty) {
      adminList.innerHTML = `
        <div class="text-center text-muted">
          <i class="fas fa-users fa-3x mb-3"></i>
          <h5>No Admin Accounts Found</h5>
          <p>Start by adding your first admin account.</p>
        </div>
      `;
      return;
    }

    let adminListHTML = `
      <div class="table-responsive">
        <table class="table table-hover">
          <thead class="table-light">
            <tr>
              <th><i class="fas fa-user"></i> Name</th>
              <th><i class="fas fa-envelope"></i> Email</th>
              <th><i class="fas fa-shield-alt"></i> Role</th>
              <th><i class="fas fa-calendar"></i> Created</th>
              <th><i class="fas fa-cogs"></i> Actions</th>
            </tr>
          </thead>
          <tbody>
    `;

    adminSnapshot.forEach((doc) => {
      const admin = doc.data();
      const isCurrentUser = admin.uid === currentUser.uid;
      const createdDate = admin.createdAt?.toDate?.() || new Date();

      adminListHTML += `
        <tr>
          <td>
            <strong>${admin.name}</strong>
            ${
              isCurrentUser
                ? '<span class="badge bg-primary ms-2">You</span>'
                : ""
            }
          </td>
          <td>${admin.email}</td>
          <td>
            <span class="badge ${
              admin.role === "super_admin" ? "bg-danger" : "bg-success"
            }">
              ${admin.role === "super_admin" ? "Super Admin" : "Admin"}
            </span>
          </td>
          <td>${createdDate.toLocaleDateString()}</td>
          <td>
            ${
              !isCurrentUser
                ? `
              <button 
                class="btn btn-sm btn-outline-danger" 
                onclick="deleteAdmin('${admin.uid}', '${admin.email}')"
                title="Delete Admin"
              >
                <i class="fas fa-trash"></i>
              </button>
            `
                : '<span class="text-muted">Cannot delete yourself</span>'
            }
          </td>
        </tr>
      `;
    });

    adminListHTML += `
          </tbody>
        </table>
      </div>
    `;

    adminList.innerHTML = adminListHTML;
  } catch (error) {
    console.error("Error loading admin list:", error);
    adminList.innerHTML = `
      <div class="alert alert-danger">
        <i class="fas fa-exclamation-triangle"></i>
        Error loading admin accounts: ${error.message}
      </div>
    `;
  }
}

// Add new admin
addAdminForm.addEventListener("submit", async (e) => {
  e.preventDefault();

  const email = document.getElementById("adminEmail").value;
  const password = document.getElementById("adminPassword").value;
  const name = document.getElementById("adminName").value;
  const role = document.getElementById("adminRole").value;

  try {
    // Create Firebase Auth user
    const userCredential = await createUserWithEmailAndPassword(
      auth,
      email,
      password
    );
    const newUser = userCredential.user;

    // Add admin record to Firestore
    await setDoc(doc(db, "admins", newUser.uid), {
      uid: newUser.uid,
      email: email,
      name: name,
      role: role,
      createdAt: serverTimestamp(),
    });

    // Sign out the new user (they should log in with their own credentials)
    await signOut(auth);

    // Sign back in as the original super admin
    // Note: In a production environment, you'd want to handle this more securely
    showMessage(`Admin account created successfully for ${email}`, "success");

    // Reset form and close modal
    addAdminForm.reset();
    const modal = bootstrap.Modal.getInstance(
      document.getElementById("addAdminModal")
    );
    modal.hide();

    // Reload admin list
    loadAdminList();
  } catch (error) {
    console.error("Error creating admin:", error);
    showMessage("Error creating admin account: " + error.message, "danger");
  }
});

// Delete admin (global function for onclick)
window.deleteAdmin = function (uid, email) {
  adminToDelete = { uid, email };
  deleteAdminEmail.textContent = email;

  const modal = new bootstrap.Modal(deleteAdminModal);
  modal.show();
};

// Confirm delete admin
confirmDeleteBtn.addEventListener("click", async () => {
  if (!adminToDelete) return;

  try {
    // Delete from Firestore first
    await deleteDoc(doc(db, "admins", adminToDelete.uid));

    // Note: Deleting Firebase Auth user requires admin SDK
    // For now, we'll just remove from Firestore
    // The user won't be able to log in since they're not in the admins collection

    showMessage(
      `Admin account for ${adminToDelete.email} has been deleted`,
      "success"
    );

    // Close modal
    const modal = bootstrap.Modal.getInstance(deleteAdminModal);
    modal.hide();

    // Reload admin list
    loadAdminList();

    adminToDelete = null;
  } catch (error) {
    console.error("Error deleting admin:", error);
    showMessage("Error deleting admin account: " + error.message, "danger");
  }
});

// Show message function
function showMessage(message, type = "info") {
  messageContainer.innerHTML = `
    <div class="alert alert-${type} alert-dismissible fade show" role="alert">
      <i class="fas fa-${
        type === "success"
          ? "check-circle"
          : type === "danger"
          ? "exclamation-triangle"
          : "info-circle"
      }"></i>
      ${message}
      <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    </div>
  `;

  // Auto-hide after 5 seconds
  setTimeout(() => {
    const alert = messageContainer.querySelector(".alert");
    if (alert) {
      const bsAlert = new bootstrap.Alert(alert);
      bsAlert.close();
    }
  }, 5000);
}
