// Firebase setup
const firebaseConfig = {
  apiKey: "AIzaSyCZ3FsgxN34goM9Crg1LlwSuxw0jUN0HrA",
  authDomain: "pybricks-website.firebaseapp.com",
  databaseURL: "https://pybricks-website-default-rtdb.firebaseio.com",
  projectId: "pybricks-website",
  storageBucket: "pybricks-website.firebasestorage.app",
  messagingSenderId: "537570597708",
  appId: "1:537570597708:web:83f2d63fef8cd802078de9",
  measurementId: "G-43CQNFDRGD"
};
firebase.initializeApp(firebaseConfig);
const db = firebase.firestore();

const idMap = {
  '/': 'home',
  '/home': 'home',
  '/start': 'start',
  '/resources': 'resources',
  '/example1': 'example1',
  '/example2': 'example2',
  '/example3': 'example3'
};

function navigate(path) {
  history.pushState(null, '', path);
  renderPage(path);
}

function renderPage(path) {
  const id = idMap[path] || 'home';

  document.querySelectorAll('.page-section').forEach(el => {
    el.style.display = 'none';
  });

  const section = document.getElementById(id);
  if (!section) return;
  section.style.display = 'block';

  // If using Firestore for content:
  loadPageFromFirestore(id);
  // Or: fetch(`data/${id}.html`) if not using Firestore
}

function loadPageFromFirestore(id) {
  history.pushState(null, '', `/${id}`);
  const pages = document.querySelectorAll('.page-section');
  pages.forEach(p => p.style.display = 'none');  // Hide all pages

  const section = document.getElementById(id);
  if (!section) return;

  // Show the section now
  section.style.display = 'block';

  db.collection("Pages").doc(id).get().then(doc => {
    if (doc.exists) {
      section.innerHTML = doc.data().html || "<p>Content not available.</p>";
      console.log(`Loaded content for ${id}`);
    } else {
      section.innerHTML = "<p style='color:red;'>Page not found.</p>";
      console.error(`No document found for ID: ${id}`);
    }
  })
    .catch(error => {
      console.error("Error fetching document:", error);
      section.innerHTML = "<p style='color:red;'>Error loading page.</p>";
    });
}

function toggleDropdown(id) {
  const dropdown = document.getElementById(id);
  dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
}

let isSignedIn = false;

// Run after DOM is loaded
window.onload = () => {
  document.getElementById('auth-btn').addEventListener('click', function () {
    isSignedIn = !isSignedIn;
    this.textContent = isSignedIn ? 'Sign Out' : 'Log In';
  });

  renderPage(window.location.pathname);
};

window.onpopstate = () => {
  renderPage(window.location.pathname);
};

// Make functions available to HTML
window.navigate = navigate;
window.loadPageFromFirestore = loadPageFromFirestore;
window.toggleDropdown = toggleDropdown;
