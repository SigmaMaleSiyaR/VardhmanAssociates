import { auth, db } from "./firebase-config.js";
import {
  onAuthStateChanged,
  signOut,
} from "https://www.gstatic.com/firebasejs/11.9.0/firebase-auth.js";
import {
  collection,
  getDocs,
  query,
  where,
} from "https://www.gstatic.com/firebasejs/11.9.0/firebase-firestore.js";

// Check if user is authenticated and is an admin
export async function checkAdminAuth() {
  return new Promise((resolve) => {
    onAuthStateChanged(auth, async (user) => {
      if (user) {
        // Check if user is in admins collection
        try {
          const adminDoc = await getDocs(
            query(collection(db, "admins"), where("uid", "==", user.uid))
          );

          if (!adminDoc.empty) {
            resolve({ isAdmin: true, user });
          } else {
            // If no admin record found, check if this is the first user
            const allAdmins = await getDocs(collection(db, "admins"));
            if (allAdmins.empty) {
              // First user becomes super admin
              resolve({ isAdmin: true, user, isFirstUser: true });
            } else {
              resolve({ isAdmin: false, user });
            }
          }
        } catch (error) {
          console.error("Error checking admin status:", error);
          resolve({ isAdmin: false, user });
        }
      } else {
        resolve({ isAdmin: false, user: null });
      }
    });
  });
}

// Check if user is super admin
export async function checkSuperAdminAuth() {
  return new Promise((resolve) => {
    onAuthStateChanged(auth, async (user) => {
      if (user) {
        try {
          const adminDoc = await getDocs(
            query(collection(db, "admins"), where("uid", "==", user.uid))
          );

          if (!adminDoc.empty) {
            const adminData = adminDoc.docs[0].data();
            resolve({ isSuperAdmin: adminData.role === "super_admin", user });
          } else {
            // If no admin record found, check if this is the first user
            const allAdmins = await getDocs(collection(db, "admins"));
            if (allAdmins.empty) {
              resolve({ isSuperAdmin: true, user, isFirstUser: true });
            } else {
              resolve({ isSuperAdmin: false, user });
            }
          }
        } catch (error) {
          console.error("Error checking super admin status:", error);
          resolve({ isSuperAdmin: false, user });
        }
      } else {
        resolve({ isSuperAdmin: false, user: null });
      }
    });
  });
}

// Redirect to login if not authenticated
export function redirectToLogin() {
  window.location.href = "/admin/index.html";
}

// Logout function
export async function logout() {
  try {
    await signOut(auth);
    window.location.href = "/admin/index.html";
  } catch (error) {
    console.error("Error logging out:", error);
  }
}

// Show authentication status in UI
export function showAuthStatus(user, isAdmin = true, isSuperAdmin = false) {
  const currentUserElement = document.getElementById("currentUser");
  const logoutBtn = document.getElementById("logoutBtn");

  if (currentUserElement) {
    currentUserElement.innerHTML = `
      <i class="fas fa-user"></i> ${user.email}
      ${
        isSuperAdmin
          ? '<span class="badge bg-danger ms-1">Super Admin</span>'
          : ""
      }
    `;
  }

  if (logoutBtn) {
    logoutBtn.addEventListener("click", async (e) => {
      e.preventDefault();
      await logout();
    });
  }
}
