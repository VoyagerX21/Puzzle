# 🧩 Django 8-Puzzle Game — Instructions & Guide

Welcome to the **Django 8-Puzzle Game**! This project is a high-performance, session-isolated, modern web puzzle game built using Django 5, Pillow, and clean JavaScript with zero external frontend framework dependencies.

---

## 🚀 Key Features & Architectural Highlights

- **🔒 Session-Based State Isolation**: Eliminates all global variables and disk mutation conflicts. Each user has an isolated game session stored securely via Django sessions.
- **⚡ Zero Page Reloads**: Dynamic client-side tile movement with background sprite positioning and asynchronous REST APIs for seamless gameplay.
- **🌓 Light / Dark Theme Support**: Default light theme with instant dark mode toggle, saved and persisted across visits via `localStorage`.
- **📸 Custom Photo Upload**: Upload any personal photo (JPG, PNG, WEBP) via drag-and-drop or file picker. Images are automatically auto-oriented, square-cropped, and transformed into an interactive puzzle using Pillow.
- **🖼️ Curated Preset Gallery**: Choose from 16 high-definition scenes categorized by theme (Landmarks, Scenery, Nature, Heritage) and difficulty.
- **🖥️ Open, Full-Screen Responsive Layout**: Spacious edge-to-edge layout that adapts naturally across desktop, tablet, and mobile devices without nested boxed clutter.
- **🔊 Web Audio API Sound Synthesizer**: Clean, unobtrusive audio feedback generated directly in-browser.
- **⌨️ Multi-Input Controls**: Mouse Click, Keyboard Navigation (`↑ ↓ ← →` and `W A S D`), and Mobile Touch Swipe gestures.
- **🧮 Solvability Verification**: Mathematical inversion counting and random-walk scrambler ensure every generated puzzle is 100% solvable.

---

## 🛠️ Prerequisites

- **Python**: `3.10` or newer (`Python 3.12` recommended)
- **pip**: Python package manager

---

## 📦 Setup & Running the Project

### 1. Clone the Repository & Switch Branch

```bash
git clone https://github.com/VoyagerX21/Puzzle.git
cd Puzzle
git checkout feature/puzzle-refactor-and-photo-upload
```

### 2. Create and Activate Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv env
.\env\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Database Migrations

```bash
python manage.py migrate
```

### 5. Start the Development Server

```bash
python manage.py runserver
```

Open your browser and navigate to:  
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🧪 Running Automated Tests

To run the automated unit test suite (covering solvability math, tile movement rules, session isolation, and custom photo uploads):

```bash
python manage.py test
```

Expected output:
```text
Found 11 test(s).
System check identified no issues (0 silenced).
...........
----------------------------------------------------------------------
Ran 11 tests in 0.040s

OK
```

---

## 🎮 How to Play

1. **Objective**: Slide the 8 tiles on the 3×3 board to recreate the image shown in the **Target Image** panel.
2. **Tile Movement**:
   - **Mouse**: Click on any tile adjacent to the blank space to slide it into the empty slot.
   - **Keyboard**:
     - `↑` or `W`: Slide the tile below the blank space up into the blank.
     - `↓` or `S`: Slide the tile above the blank space down into the blank.
     - `←` or `A`: Slide the tile to the right of the blank space left into the blank.
     - `→` or `D`: Slide the tile to the left of the blank space right into the blank.
   - **Mobile Touch**: Swipe left, right, up, or down across the board.
3. **Assistance & Features**:
   - **Hold to Peek**: Press and hold to project a translucent reference overlay directly over the puzzle board.
   - **Show Numbers**: Display numerical badges (1–8) on tiles for easier sequencing.
   - **Scramble Level**: Select between *Easy* (20 moves), *Medium* (45 moves), and *Hard* (90 moves).
   - **Shuffle**: Scramble the current puzzle into a guaranteed solvable state and reset the timer/counter.
   - **Theme Toggle**: Switch between Light Mode and Dark Mode at any time in the navigation bar.

---

## 📸 Uploading Your Own Photo

1. Click the **"Upload Photo"** button in the top navigation bar or in the presets gallery.
2. Drag and drop an image or click to select a file from your computer.
3. Review the preview and click **"Create Puzzle"**.
4. The server validates and square-crops the image, and your custom puzzle starts immediately!

---

## 📂 Project Structure

```text
Puzzle/
├── manage.py                   # Django CLI entrypoint
├── requirements.txt            # Python dependencies (Django, Pillow, numpy, etc.)
├── .gitignore                  # Git ignore rules for Python, SQLite, media uploads
├── instructions.md             # Complete running and usage guide
├── README.md                   # Project overview
├── Puzzle/                     # Project configuration
│   ├── settings.py             # Django settings (sessions, static/media, security)
│   ├── urls.py                 # Root URL routing
│   ├── wsgi.py                 # WSGI application entrypoint
│   └── asgi.py                 # ASGI application entrypoint
├── myapp/                      # Puzzle game application
│   ├── admin.py                # Admin site configuration
│   ├── apps.py                 # App configuration
│   ├── forms.py                # Photo upload form validation
│   ├── models.py               # Models
│   ├── tests.py                # Unit test suite (11 tests)
│   ├── urls.py                 # Application routing and REST API endpoints
│   ├── utils.py                # Solvability math, Pillow image processor, presets catalog
│   ├── views.py                # Session-backed view handlers & JSON API endpoints
│   ├── static/                 # Static assets
│   │   └── myapp/
│   │       ├── css/style.css   # Classic responsive stylesheet (Light / Dark themes)
│   │       └── js/game.js      # Zero-reload game engine, theme manager, audio synth
│   └── templates/              # HTML5 Templates
│       └── myapp/
│           ├── index.html      # Main puzzle board template
│           └── choice.html     # Presets catalog template
└── media/                      # Media storage
    ├── myapp/images/           # Curated preset scenes (1..16)
    └── uploads/                # User custom uploaded images (session-scoped)
```

---

## 📡 REST API Reference

| Endpoint | Method | Description |
| :--- | :---: | :--- |
| `GET /` | `GET` | Main game view (renders `index.html` with initial session state) |
| `GET /choices/` | `GET` | Gallery view for preset image selection |
| `GET /api/state/` | `GET` | Returns current session game state as JSON |
| `POST /api/move/` | `POST` | Validates & applies tile move (`{"tile_index": int}`) |
| `POST /api/shuffle/` | `POST` | Scrambles current board (`{"difficulty": "easy"\|"medium"\|"hard"}`) |
| `POST /api/select-preset/`| `POST` | Selects preset image by ID (`{"id": int}`) |
| `POST /api/upload-photo/` | `POST` | Multipart upload for custom photo (`photo` file) |
| `POST /api/reset/` | `POST` | Resets and re-shuffles current puzzle |
