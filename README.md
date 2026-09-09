# 🧩 Django 8-Puzzle Game

<p align="center">
  <a href="https://bing.khakse.dev" target="_blank">
    <img src="https://img.shields.io/badge/Live%20Demo-bing.khakse.dev-2ea44f?style=for-the-badge&logo=azure&logoColor=white" alt="Live Demo" />
  </a>
  <a href="https://hub.docker.com/r/voyagerx21/puzzle-game" target="_blank">
    <img src="https://img.shields.io/badge/Docker%20Hub-voyagerx21%2Fpuzzle--game%3Alatest-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker Hub" />
  </a>
  <img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Django-5.0+-092E20?style=for-the-badge&logo=django&logoColor=white" alt="Django" />
  <img src="https://img.shields.io/badge/Tests-11%20Passing-brightgreen?style=for-the-badge&logo=checkmarx&logoColor=white" alt="Tests" />
</p>

---

## 🌟 Overview

Welcome to the **Django 8-Puzzle Game** — a high-performance, session-isolated, modern web puzzle game built with **Python**, **Django**, **Pillow**, and clean Vanilla JS/CSS. 

Solve scrambled 3×3 sliding tile puzzles, pick from curated preset galleries, or **upload your own custom photos** with instant square cropping and auto-orientation. Guaranteed 100% solvable every time through mathematical parity validation and random-walk scrambling!

👉 **Play Live Demo:** [**https://bing.khakse.dev**](https://bing.khakse.dev)  
🐳 **Docker Image:** [`voyagerx21/puzzle-game:latest`](https://hub.docker.com/r/voyagerx21/puzzle-game)

---

## 📷 Gameplay & Demo

<p align="center">
  <img src="media/myapp/refs/Screenshot%202026-09-09%20104510.png" alt="Light Theme Gameplay" width="85%" />
  <br />
  <em>🎮 Responsive Board with Step Counter, Timer, Peek Hint & Numbers Toggle (Light Theme)</em>
</p>

<p align="center">
  <img src="media/myapp/refs/Screenshot%202026-09-09%20104527.png" alt="Dark Theme Gameplay" width="85%" />
  <br />
  <em>🌙 Instant Dark Mode Toggle with Translucent Board and Visual Hints</em>
</p>

<p align="center">
  <img src="media/myapp/refs/Screenshot%202026-09-09%20104803.png" alt="Curated Preset Gallery" width="85%" />
  <br />
  <em>🖼️ Categorized Preset Gallery (Landmarks, Scenery, Nature, Heritage) & Custom Photo Upload</em>
</p>

---

## 🚀 Features

- 🧩 **Classic 3×3 Sliding Puzzle**: 8 tiles with 1 blank space and smooth CSS transition animations.
- 📸 **Custom Photo Upload**: Upload any personal image (JPG, PNG, WEBP) with automatic EXIF orientation and Pillow square-cropping.
- 🖼️ **Curated Presets Gallery**: 16 high-definition scenes across Landmarks, Scenery, Nature, and Heritage.
- 🔒 **Session-Isolated Architecture**: Multi-user friendly with zero disk-mutation conflicts or race conditions.
- 🌓 **Instant Dark & Light Theme**: Seamless toggle persisted across visits via `localStorage`.
- 🧮 **100% Solvability Guarantee**: Solvability verification via inversion counting and randomized valid-move walks.
- 👁️ **Peek Hint & Number Badges**: Press and hold to view translucent reference overlay or toggle number guides (1–8).
- ⌨️ **Multi-Input Controls**:
  - 🖱️ **Mouse Click**: Click adjacent tiles to slide.
  - ⌨️ **Keyboard**: `W A S D` or `Arrow Keys` (`↑ ↓ ← →`).
  - 📱 **Mobile Touch**: Swipe left, right, up, or down.
- ⏱️ **Timer & Step Counter**: Real-time elapsed time tracking, step count, and celebration win screen.
- 🔊 **Web Audio Sound Effects**: Low-latency, browser-synthesized audio feedback (no external audio assets required).

---

## 🐳 Quick Start with Docker

You can run the application instantly with Docker without installing Python or dependencies.

### 1. Run with Docker CLI

```bash
docker run -d \
  --name puzzle-web \
  --restart unless-stopped \
  -p 8888:8888 \
  -e PORT=8888 \
  -e ALLOWED_HOSTS="*" \
  -v puzzle_media:/app/media \
  -v puzzle_db:/app/data \
  voyagerx21/puzzle-game:latest
```

Open your browser at **[http://localhost:8888](http://localhost:8888)**.

### 2. Run with Docker Compose

```yaml
services:
  web:
    image: voyagerx21/puzzle-game:latest
    container_name: puzzle_web
    restart: unless-stopped
    ports:
      - "8888:8888"
    environment:
      - PORT=8888
      - DEBUG=False
      - ALLOWED_HOSTS=*
    volumes:
      - puzzle_media:/app/media
      - puzzle_db:/app/data

volumes:
  puzzle_media:
    driver: local
  puzzle_db:
    driver: local
```

Start the service:
```bash
docker compose up -d
```

---

## 🔧 Local Development Setup

### 1. Clone the repository

```bash
git clone https://github.com/VoyagerX21/Puzzle.git
cd Puzzle
```

### 2. Create and activate virtual environment

**Windows:**
```powershell
python -m venv env
.\env\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv env
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply migrations

```bash
python manage.py migrate
```

### 5. Start the development server

```bash
python manage.py runserver
```

Open **[http://127.0.0.1:8888/](http://127.0.0.1:8888/)** in your browser.

---

## 🧪 Running Automated Tests

The test suite validates game logic, solvability mathematics, REST endpoints, session isolation, and image uploads:

```bash
python manage.py test
```

---

## 🧠 How to Play

1. **Choose a Picture**: Select a scene from the preset gallery or upload your own photo.
2. **Select Difficulty & Shuffle**: Pick *Easy* (20 moves), *Medium* (45 moves), or *Hard* (90 moves) and click **Shuffle**.
3. **Slide the Tiles**: Move tiles into the blank space using mouse clicks, arrow keys / WASD, or touch swipes.
4. **Use Visual Aids**:
   - Hold the **"Hold to Peek"** button to view the target image overlay.
   - Click **"Show Numbers"** for numerical tile ordering guides.
5. **Win**: Complete the original image in the fewest steps and fastest time!

---

## 📂 Project Structure

```text
Puzzle/
├── manage.py                   # Django management entrypoint
├── Dockerfile                  # Container build instructions
├── docker-compose.yml          # Compose service configuration
├── Makefile                    # Build & push automation shortcuts
├── requirements.txt            # Python dependencies
├── instructions.md             # Developer guide & instructions
├── deployment.md               # Azure VM deployment guide
├── Puzzle/                     # Core Django project settings
│   ├── settings.py             # Settings (session, static/media, security)
│   ├── urls.py                 # Root URL routing
│   └── wsgi.py                 # WSGI application entrypoint
├── myapp/                      # 8-Puzzle game application
│   ├── tests.py                # Unit tests for game logic & upload validation
│   ├── urls.py                 # REST API endpoints & view routes
│   ├── utils.py                # Solvability math, Pillow image processor, presets catalog
│   ├── views.py                # Session-backed handlers & JSON API endpoints
│   ├── static/myapp/
│   │   ├── css/style.css       # Responsive design with Light & Dark themes
│   │   └── js/game.js          # Zero-reload game engine & Web Audio synthesizer
│   └── templates/myapp/
│       ├── index.html          # Main game board template
│       └── choice.html         # Preset selection gallery
└── media/
    ├── myapp/images/           # 16 Curated preset puzzle images
    ├── myapp/refs/             # Demo screenshots & references
    └── uploads/                # User uploaded custom images
```

---

## 🌐 Deployment Details

- **Host**: Azure Virtual Machine (Ubuntu / Docker)
- **Live URL**: [**https://bing.khakse.dev**](https://bing.khakse.dev)
- **Container Registry**: [**Docker Hub (`voyagerx21/puzzle-game:latest`)**](https://hub.docker.com/r/voyagerx21/puzzle-game)
- Refer to [`deployment.md`](deployment.md) for full Azure VM setup, Nginx reverse proxy, and SSL instructions.

---

## 🤝 Credits & Acknowledgements

- Designed and developed by **[VoyagerX21](https://github.com/VoyagerX21)**.
- Frontend styling contributions by **[Kunal-rawat](https://github.com/Kunal-Rawat007)**.
- Built with **[Django](https://www.djangoproject.com/)** and **[Pillow](https://python-pillow.org/)**.