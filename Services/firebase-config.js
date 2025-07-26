// Firebase configuration and initialization
import { initializeApp } from "https://www.gstatic.com/firebasejs/11.9.0/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/11.9.0/firebase-auth.js";
import { getFirestore } from "https://www.gstatic.com/firebasejs/11.9.0/firebase-firestore.js";

const firebaseConfig = {
  apiKey: "AIzaSyAV6RSeZ1j5krYodWKIXGNJE1sY_l9pvh8",
  authDomain: "vardhamanassociates-861f9.firebaseapp.com",
  projectId: "vardhamanassociates-861f9",
  storageBucket: "vardhamanassociates-861f9.firebasestorage.app",
  messagingSenderId: "322122751719",
  appId: "1:322122751719:web:9f4ae6936a8bf144244c42",
  measurementId: "G-Y06T3Q22YD",
};

const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

export { app, auth, db }; 