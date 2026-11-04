# CampusGPT – Your Smart LPU Campus Companion 🎓🤖

An enterprise-grade, native-feeling mobile application exclusively designed for **Lovely Professional University (LPU)** students, faculty, and campus visitors.

CampusGPT brings together an intelligent **Gemini RAG AI chatbot**, **smart timetable conflict detection**, **75% attendance predictor**, **campus navigation with QR scanning**, **PyMuPDF-powered study assistant**, **lost-and-found student board**, **event finder**, and **AI placement career accelerator**.

---

## 🏗️ Architecture & Technology Stack

```
CampusGPT/
├── mobile/                   # React Native + Expo (SDK 52) + TypeScript
│   ├── src/
│   │   ├── components/       # Button, Card, Header, Input, Skeleton, Badge, CircularProgress
│   │   ├── context/          # AuthContext, ThemeContext (Light & Dark mode)
│   │   ├── navigation/       # AppNavigator, BottomTabNavigator, AuthNavigator
│   │   ├── screens/          # 8 Main Module Screens + Auth & Sub-screens
│   │   ├── services/         # API Client, Secure Storage, Mock Fallback Data
│   │   ├── theme/            # LPU Navy Blue, Royal Purple, Slate Dark Themes
│   │   └── types/            # Strict TypeScript Interfaces
│   ├── app.json              # Expo configuration, permissions, adaptive icons
│   └── package.json
│
└── backend/                  # Python 3.13 + Django 6.1 + Django REST Framework
    ├── accounts/             # Registration, token login, student profile (Reg No, course, section)
    ├── chatbot/              # Gemini RAG assistant, verified LPU facts repository, history
    ├── timetable/            # Weekly schedule, next class detector, conflict detection
    ├── attendance/           # Subject attendance tracker & 75% target predictor
    ├── navigation/           # Verified LPU building GPS coordinates & QR code directory
    ├── study_assistant/      # PyMuPDF extraction, chapter summary, MCQs, flashcards
    ├── lost_found/           # Lost & found noticeboard, claims, photo uploads
    ├── events/               # HackLPU, Youth Vibe, workshops, bookmarks
    ├── career/               # Resume ATS score, technical & HR interview prep, roadmap
    ├── notifications/        # In-app push alerts, study partner matching & "My Campus Day"
    ├── services/             # AI layer: Ollama local, Ollama cloud, Google Gemini (llm_service.py)
    └── manage.py
```

---

## 🚀 Quick Start Guide

### 1. Backend Setup & Run

```bash
# Navigate to backend directory
cd backend

# Install Python requirements (if not already installed)
pip install -r requirements.txt

# Run migrations (already generated and verified)
python manage.py migrate

# Seed database with realistic LPU courses, timetable, faculty, and locations
python seed_data.py

# Run all 13 automated endpoint tests
python test_all_endpoints.py

# Start Django development server
python manage.py runserver 0.0.0.0:8000
```

> **MySQL Configuration:**  
> The backend connects to MySQL when `USE_MYSQL=True` in `backend/.env`. It uses PyMySQL drivers and gracefully falls back to SQLite for instant local testing without setup overhead.

> **Google Gemini API Key:**  
> Add your key to `backend/.env`:  
> `GEMINI_API_KEY=your_actual_key_here`  
> Supported models: `gemini-1.5-flash`, `gemini-2.0-flash`, `gemini-1.5-pro`.

---

### AI Providers (Ollama Local + Ollama Cloud + Gemini)

The chatbot, study assistant and career module all go through `backend/services/llm_service.py`.
With `AI_PROVIDER=auto` it tries **Ollama local -> Ollama cloud -> Gemini** and uses the first that answers;
if none are reachable it falls back to the built-in verified-answer engine, so the app never breaks.

**Local Ollama** (runs on the computer that runs Django):
```bash
# install from https://ollama.com, then
ollama pull llama3.2
ollama serve          # skip if the Ollama app is already running
```
**Ollama Cloud:** create a key at https://ollama.com/settings/keys and set `OLLAMA_API_KEY` in `backend/.env`
(default cloud model: `gpt-oss:120b`, change with `OLLAMA_CLOUD_MODEL`).

Relevant `backend/.env` keys: `AI_PROVIDER`, `OLLAMA_HOST`, `OLLAMA_MODEL`, `OLLAMA_TIMEOUT`,
`OLLAMA_CLOUD_HOST`, `OLLAMA_CLOUD_MODEL`, `OLLAMA_API_KEY`, `GEMINI_API_KEY`.

Check what is reachable: `GET /api/v1/chatbot/providers/`. In the app, the chat screen has an
**Auto / Local / Cloud / Gemini** picker with a green/red availability dot for each.
The phone never talks to Ollama directly - only the Django backend does.

---

### 2. Mobile App Setup & Run (React Native / Expo)

```bash
# Navigate to mobile directory
cd mobile

# Install dependencies
npm install

# Camera for the QR scanner (picks the version that matches your Expo SDK)
npx expo install expo-camera

# Start Expo development server
npm run start
```

#### Running on Android Emulator:
Press `a` in the Expo terminal or run:
```bash
npx expo run:android
```

#### Running on a Physical Android Phone:
1. Install **Expo Go** from Google Play Store on your Android phone.
2. Ensure phone and computer are on the same Wi-Fi network.
3. In `mobile/src/services/api.ts`, update `DEFAULT_BASE_URL` with your computer's local Wi-Fi IP:  
   `http://<YOUR_COMPUTER_LAN_IP>:8000/api/v1`
4. Scan the QR code displayed in the Expo terminal with your phone camera or Expo Go.

---

### 3. Generating Standalone Android APK (EAS Build)

To build a standalone installable `.apk` file for Android:

```bash
# 1. Install EAS CLI globally
npm install -g eas-cli

# 2. Login to your Expo account
eas login

# 3. Configure EAS Build
eas build:configure

# 4. Generate standalone Android APK
eas build -p android --profile preview
```

The resulting `.apk` can be installed on any Android phone directly without needing Expo Go.

---

### 4. Preparing for iOS Build

To prepare and build for iOS (Apple TestFlight / App Store):

```bash
# For local iOS Simulator (requires macOS with Xcode)
npx expo run:ios

# For production iOS build via EAS Cloud
eas build -p ios
```

The `mobile/app.json` is preconfigured with the required iOS permissions:
- `NSCameraUsageDescription` for campus QR scanning and lost-and-found photos.
- `NSLocationWhenInUseUsageDescription` for walking navigation on campus.
- `NSPhotoLibraryUsageDescription` for PDF study document uploads.

---

## 📱 The Eight Powerful Modules

1. **Ask Anything About LPU (Gemini RAG Chatbot):**  
   Real-time answers on examination criteria, hostel curfew rules, central library hours, and course guidelines. Never hallucinates; cites official university documents. Supports text-to-speech and suggested prompts.

2. **Smart Timetable:**  
   Weekly day-by-day timetable with automatic schedule conflict detection, room codes (e.g., Block 34-402, 27-407), assigned faculty contacts, and next upcoming class countdown on the home dashboard.

3. **Attendance Predictor:**  
   Circular progress indicator tracking the university's 75% attendance threshold. Interactive simulator calculates the exact consecutive classes needed to exit shortage or maximum classes you can safely miss.

4. **Campus Navigation:**  
   Interactive directory of verified LPU blocks (Blocks 25-38, Unipolis, UniMall, Central Library, UniHospital, BH/GH Hostels) with coordinates, walking directions, and camera QR code lookup.

5. **Study Assistant:**  
   Upload PDFs or lecture notes. Powered by PyMuPDF and Gemini to extract text, summarize chapters, generate interactive 4-choice MCQs quizzes, and revision flashcards with 3D flip animation.

6. **Lost and Found Community:**  
   Report lost or found items with photo attachments, category filters, searchable noticeboard, and ownership claim submission.

7. **Event Finder:**  
   Discover HackLPU hackathons, technical workshops, placement briefings, and Youth Vibe fests. Bookmark events and access official registration links.

8. **Career Assistant:**  
   AI resume review with ATS score (0-100), customized improvement tips, technical & HR interview questions with model answers, and structured 8-week placement roadmap.

---

## 🔐 Credentials for Testing

- **Demo Student Registration Number:** `12204567`
- **Demo Student Password:** `Student@123`
- **Course:** B.Tech Computer Science & Engineering (Section K22DF)
- **Django Admin:** `http://localhost:8000/admin/`
