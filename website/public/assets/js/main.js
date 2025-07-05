const idMap = {
  'home': 'home',
  'start': 'start',
  'resources': 'resources',
  'example1': 'examples/example1',
  'example2': 'examples/example2',
  'example3': 'examples/example3',
  'hubs': 'learn/hubs',
  'motors': 'learn/motors',
  'sensors': 'learn/sensors',
  'learn': 'learn/index'
};

// Firebase config (unchanged)
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

// Load Markdown from .md file
async function loadMarkdownContent(id) {
  const section = document.getElementById('markdown-content');
  if (!section) return;

  try {
    const response = await fetch(`assets/pages/${id}.md`);
    if (!response.ok) throw new Error();
    const md = await response.text();
    section.innerHTML = marked.parse(md);
  } catch (e) {
    section.innerHTML = `<p style="color:red;">Page not found: ${id}</p>`;
  }
}

// Load from Firestore (for future account manager use)
async function loadFromFirestore(collectionName, docId) {
  const section = document.getElementById('markdown-content');
  if (!section) return;

  try {
    const doc = await db.collection(collectionName).doc(docId).get();
    if (doc.exists) {
      section.innerHTML = marked.parse(doc.data().markdown || 'No content.');
    } else {
      section.innerHTML = "<p style='color:red;'>Document not found.</p>";
    }
  } catch (e) {
    section.innerHTML = "<p style='color:red;'>Error loading Firestore content.</p>";
    console.error(e);
  }
}

// Navigation handler
function navigate(name) {
  const id = idMap[name] || 'home';
  history.pushState({}, '', `/${name}`);
  loadMarkdownContent(id);
}

// Sidebar dropdown toggle
function toggleDropdown(id) {
  const dropdown = document.getElementById(id);
  if (dropdown) {
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
  }
}

// Make available to HTML
window.navigate = navigate;
window.toggleDropdown = toggleDropdown;
window.loadFromFirestore = loadFromFirestore;

// Handle browser nav
window.onpopstate = () => {
  const path = window.location.pathname.slice(1) || 'home';
  navigate(path);
};

// Initial load
document.addEventListener('DOMContentLoaded', () => {
  const path = window.location.pathname.slice(1) || 'home';
  navigate(path);
});
