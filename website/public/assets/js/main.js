const idMap = {
  'home': '../assets/pages/home',
  'start': '../assets/pages/start',
  'resources': '../assets/pages/resources',
  'example1': '../assets/pages/examples/example1',
  'example2': '../assets/pages/examples/example2',
  'example3': '../assets/pages/examples/example3',
  'hubs': '../assets/pages/learn/hubs',
  'motors': '../assets/pages/learn/motors',
  'sensors': '../assets/pages/learn/sensors',
};

const urlMap = {
  'home': 'home',
  'start': 'start',
  'resources': 'resources',
  'example1': 'examples/example1',
  'example2': 'examples/example2',
  'example3': 'examples/example3',
  'hubs': 'learn/hubs',
  'motors': 'learn/motors',
  'sensors': 'learn/sensors',
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
async function goTo(page, path) {
  const container = document.getElementById("content"); // Your main content area
  const filePath = `${path}.html`;

  try {
    const res = await fetch(filePath);
    if (!res.ok) throw new Error("Page not found");

    const html = await res.text();
    container.innerHTML = html;
    console.log(`Loaded ${page}`);
    rewriteURL(urlMap[page] || 'home');
    setTimeout(() => {
      setupCopyButtons();
    }, 200);
  } catch (err) {
    console.error(err);
    container.innerHTML = `<h1>Error loading page</h1><p>${err.message}</p>`;
    rewriteURL('error');
  }
}

function navigate(page) {
  const fullPath = idMap[page] || 'home';
  console.log(`Navigating to: ${page}`);
  goTo(page, fullPath);

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

document.addEventListener("DOMContentLoaded", () => {
  const path = window.location.pathname.replace(/^\/+|\/+$/g, ''); // remove slashes
  const idMap = {
    "home": "home",
    "about": "about",
    "resources": "resources",
    "examplesexample1": "example1",
    "examplesexample2": "example2",
    "examplesexample3": "example3",

  };
  if (idMap[path]) {
    navigate(idMap[path]); // navigate to valid page
  } else {
    window.location.href = "/404.html"; // redirect to 404 page
  }
});
function setupCopyButtons() {
  console.log("🔍 Looking for copy buttons...");

  // Remove old listeners by cloning nodes
  document.querySelectorAll(".copy-btn").forEach(btn => {
    const newBtn = btn.cloneNode(true);
    btn.parentNode.replaceChild(newBtn, btn);
  });

  // Attach listeners
  document.querySelectorAll(".copy-btn").forEach(copyBtn => {
    const targetSelector = copyBtn.getAttribute("data-target");
    const codeBlock = document.querySelector(targetSelector);

    if (!codeBlock) {
      console.warn(`⚠️ No code block found for ${targetSelector}`);
      return;
    }

    copyBtn.addEventListener("click", () => {
      console.log(`📋 Copy button clicked for ${targetSelector}`);
      navigator.clipboard.writeText(codeBlock.innerText)
        .then(() => console.log("✅ Code copied to clipboard"))
        .catch(err => console.error("❌ Copy failed", err));
    });

    console.log(`✅ Copy listener attached for ${targetSelector}`);
  });
}
