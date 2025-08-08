const idMap = {
  'home': '../home',
  'start': '../start',
  'resources': '../resources',
  'example1': 'examples/example1',
  'example2': 'examples/example2',
  'example3': 'examples/example3',
  'hubs': 'learn/hubs',
  'motors': 'learn/motors',
  'sensors': 'learn/sensors',
  'learn': 'learn/index'
};

// Firebase config
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

// SPA-style navigation
async function goTo(page) {
  const container = document.getElementById("content"); // Your main content area
  const filePath = `${page}.html`;

  try {
    const res = await fetch(filePath);
    if (!res.ok) throw new Error("Page not found");

    const html = await res.text();
    container.html = html;
    console.log(`Loaded ${filePath}`);
    rewriteURL(page);
  } catch (err) {
    console.error(err);
    container.innerHTML = `<h1>404 - Page Not Found</h1><p>The page you are looking for does not exist.</p>`;
  }
}

function navigate(path) {
  const page = idMap[path] || 'home';
  console.log(`Navigating to: ${page}`);
  goTo(page);
}

function rewriteURL(name) {
  console.log(`Rewriting URL to: /${name}`);
  history.pushState({}, '', `/${name}`);
}

function toggleDropdown(id) {
  const dropdown = document.getElementById(id);
  if (dropdown) {
    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
  }
}

// Browser back/forward
window.onpopstate = () => {
  const path = window.location.pathname.slice(1) || 'home';
  navigate(path);
};

// Initial load
document.addEventListener('DOMContentLoaded', () => {
  const path = window.location.pathname.slice(1) || 'home';
  navigate(path);
});
