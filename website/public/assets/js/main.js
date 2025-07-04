// Firebase setup
const fireStoreNames = {
  collections: {
    MainPage: "Pages",
    LearnPage: "Learn"
  },
  pages: {
    home: "home",
    start: "start",
    resources: "resources",
    example1: "example1",
    example2: "example2",
    example3: "example3"
  },
  LearnPages: {
    Hubs: "Hubs",
    Motors: "SpikePrime",
    Sensors: "Sensors",
  }
}
const idMap = {
  '/': 'home',
  '/home': 'home',
  '/start': 'start',
  '/resources': 'resources',
  '/example1': 'example1',
  '/example2': 'example2',
  '/example3': 'example3',
  '/learn/hubs': 'Hubs',
  '/learn/motors': 'Motors',
  '/learn/sensors': 'Sensors',
  '/learn': 'Learn',
}


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


function loadFromFirestore(collectionName, docId) {
    db.collection(collectionName).doc(docId).get().then(doc => {
      if (doc.exists) {
        const data = doc.data();
        return data;
      } else {
        return "Data not found";
      }
    });
}


function toggleDropdown(id) {
  const dropdown = document.getElementById(id);
  dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
}

function loadMarkdownContent(id) {
  fetch(`pages/${id}.md`)
    .then(res => {
      if (!res.ok) throw new Error();
      return res.text();
    })
    .then(md => {
      section.innerHTML = marked.parse(md);
    })
    .catch(() => {
      section.innerHTML = '<p style="color:red;">Page not found.</p>';
    });
}

function navigate(name) {
  const id = idMap[name] || 'home';
  history.pushState({}, '', `/${id}`);
  loadMarkdownContent(name);
}


// Make functions available to HTML
window.navigate = navigate;
window.loadFromFirestore = loadFromDatabase;
window.toggleDropdown = dropdown;
