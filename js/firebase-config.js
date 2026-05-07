// Your web app's Firebase configuration
const firebaseConfig = {
  apiKey: "AIzaSyDxPLNj-4c0DuHnJDxj2V9KRQtNVW1DKn0",
  authDomain: "cars-38576.firebaseapp.com",
  projectId: "cars-38576",
  storageBucket: "cars-38576.firebasestorage.app",
  messagingSenderId: "513751416718",
  appId: "1:513751416718:web:0e5f94b3b087b0da966edf",
  measurementId: "G-3DXMXK495Q"
};

// Initialize Firebase (Using Compat SDK so it works seamlessly with our existing auth scripts)
firebase.initializeApp(firebaseConfig);
const auth = firebase.auth();
const db = firebase.firestore();
