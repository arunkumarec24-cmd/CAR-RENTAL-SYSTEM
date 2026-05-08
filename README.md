# 🚗 Velox Rentals — Setup & Deployment Guide

> Premium car rental web app with Firebase Authentication (Google Sign-In + Email/Password) and Firestore cloud bookings.

---

## 📁 Project Structure

```
velox-rentals/
├── index.html         ← Login page (Google + Email auth)
├── app.html           ← Main car rental application
├── firebase-config.js ← Your Firebase credentials (edit this!)
└── README.md          ← This file
```

---

## 🔥 STEP 1 — Create a Firebase Project

1. Go to **https://console.firebase.google.com**
2. Click **"Add project"** → Name it `velox-rentals` → Continue
3. Disable Google Analytics (optional) → **Create project**

---

## 🔐 STEP 2 — Enable Authentication

1. In Firebase Console → **Authentication** → **Get started**
2. Click **Sign-in method** tab
3. Enable **Google** → Set support email → Save
4. Enable **Email/Password** → Save

---

## 🗄️ STEP 3 — Create Firestore Database

1. In Firebase Console → **Firestore Database** → **Create database**
2. Choose **Start in test mode** (for development) → Next
3. Select your nearest region → **Enable**

### Set Firestore Security Rules (after testing):
Go to **Firestore → Rules** and paste:
```
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    match /bookings/{bookingId} {
      allow read, write: if request.auth != null && request.auth.uid == resource.data.userId;
      allow create: if request.auth != null && request.auth.uid == request.resource.data.userId;
    }
  }
}
```

---

## ⚙️ STEP 4 — Get Your Firebase Config

1. In Firebase Console → **Project Settings** (gear icon) → **General**
2. Scroll to **"Your apps"** → Click **Web** icon (`</>`)
3. Register app name: `velox-web` → **Register app**
4. Copy the `firebaseConfig` object values

Open `firebase-config.js` and replace the placeholder values:
```javascript
const FIREBASE_CONFIG = {
  apiKey: "AIzaSy...",           // ← paste your actual values
  authDomain: "your-app.firebaseapp.com",
  projectId: "your-project-id",
  storageBucket: "your-app.appspot.com",
  messagingSenderId: "123456789",
  appId: "1:123456789:web:abc123"
};
```

---

## 🐙 STEP 5 — Host on GitHub Pages

### 5a. Create a GitHub Repository

1. Go to **https://github.com/new**
2. Repository name: `velox-rentals`
3. Set to **Public**
4. Click **Create repository**

### 5b. Upload files

**Option A — Upload via browser (easiest):**
1. Open your new repo on GitHub
2. Click **"uploading an existing file"**
3. Drag & drop all 3 files: `index.html`, `app.html`, `firebase-config.js`
4. Click **Commit changes**

**Option B — Git command line:**
```bash
git init
git add .
git commit -m "Initial commit - Velox Rentals"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/velox-rentals.git
git push -u origin main
```

### 5c. Enable GitHub Pages

1. Go to your repo → **Settings** → **Pages**
2. Under **Source**, select **Deploy from a branch**
3. Branch: `main` / Folder: `/ (root)` → **Save**
4. Wait ~2 minutes → Your site will be live at:
   ```
   https://YOUR_USERNAME.github.io/velox-rentals/
   ```

---

## 🌐 STEP 6 — Add GitHub Pages Domain to Firebase

1. Firebase Console → **Authentication** → **Settings** → **Authorized domains**
2. Click **Add domain**
3. Add: `YOUR_USERNAME.github.io`
4. Save

> ⚠️ Without this step, Google Sign-In will fail with an "unauthorized domain" error!

---

## ✅ Final Checklist

- [ ] `firebase-config.js` filled with real credentials
- [ ] Google Auth enabled in Firebase
- [ ] Email/Password Auth enabled in Firebase
- [ ] Firestore database created in test mode
- [ ] Firestore security rules updated
- [ ] All 3 files uploaded to GitHub
- [ ] GitHub Pages enabled
- [ ] `YOUR_USERNAME.github.io` added to Firebase Authorized domains

---

## 🔗 Your Live URLs

After deployment:
- **Login page:** `https://YOUR_USERNAME.github.io/velox-rentals/`
- **App:** `https://YOUR_USERNAME.github.io/velox-rentals/app.html`

---

## 🛠️ Troubleshooting

| Problem | Fix |
|---|---|
| Google Sign-In fails | Add GitHub Pages domain to Firebase Authorized domains |
| "Firebase not defined" | Check `firebase-config.js` is in same folder |
| Bookings not loading | Check Firestore rules + check browser console |
| Redirect loop | Clear browser cache, check `index.html` is the default file |
| CORS errors | These are normal in local file:// — must test on live URL |

---

## 💡 Testing Locally

Firebase Auth **does not work** when opening HTML files directly (`file://`). You need a local server:

```bash
# If you have Python:
python -m http.server 8000
# Then open: http://localhost:8000

# If you have Node.js:
npx serve .
# Then open: http://localhost:3000
```

Add `localhost` to Firebase Authorized domains for local testing.
