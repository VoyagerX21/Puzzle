/**
 * Django 8-Puzzle Game Engine
 * Classic UI, Light/Dark Theme Management, Zero Page Reloads
 */

class PuzzleGame {
  constructor() {
    this.boardEl = document.getElementById('puzzle-board');
    this.movesEl = document.getElementById('stat-moves');
    this.timerEl = document.getElementById('stat-timer');
    this.hintImgEl = document.getElementById('hint-img');
    this.hintTitleEl = document.getElementById('hint-title');
    this.ghostOverlay = document.getElementById('ghost-overlay');
    this.difficultyBadge = document.getElementById('difficulty-badge');
    this.boardContainer = document.getElementById('board-container');

    // State
    this.state = window.INITIAL_GAME_STATE || {
      board: [1, 2, 3, 4, 5, 6, 7, 8, 9],
      moves: 0,
      is_solved: false,
      image_url: '/media/myapp/images/img7.png',
      image_title: 'Sydney Opera House',
      difficulty: 'medium',
      is_custom: false,
    };

    this.soundEnabled = localStorage.getItem('puzzle_sound') === 'true'; // Default sound off for classic calm experience
    this.timerInterval = null;
    this.secondsElapsed = 0;
    this.isTimerRunning = false;
    this.showNumbers = false;
    this.isProcessingMove = false;

    // Initialize Theme
    this.initTheme();

    // Audio Context
    this.initAudio();

    // Initialize DOM and controls
    this.initDOM();
    this.initKeyboard();
    this.initTouch();
    this.initModals();
    this.render();
    this.startTimer();
  }

  /* ==========================================================================
     Theme Management (Default: Light Theme, LocalStorage Persisted)
     ========================================================================== */
  initTheme() {
    const savedTheme = localStorage.getItem('puzzle_theme') || 'light';
    this.setTheme(savedTheme);

    const themeBtn = document.getElementById('btn-theme');
    if (themeBtn) {
      this.updateThemeButton(themeBtn, savedTheme);
      themeBtn.addEventListener('click', () => {
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
        const nextTheme = currentTheme === 'light' ? 'dark' : 'light';
        this.setTheme(nextTheme);
        this.updateThemeButton(themeBtn, nextTheme);
      });
    }
  }

  setTheme(theme) {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('puzzle_theme', theme);
  }

  updateThemeButton(button, theme) {
    if (!button) return;
    button.textContent = theme === 'light' ? 'Dark Mode' : 'Light Mode';
  }

  /* ==========================================================================
     Audio Synthesizer (Web Audio API)
     ========================================================================== */
  initAudio() {
    try {
      const AudioContext = window.AudioContext || window.webkitAudioContext;
      this.audioCtx = new AudioContext();
    } catch (e) {
      this.audioCtx = null;
    }
  }

  ensureAudioContext() {
    if (this.audioCtx && this.audioCtx.state === 'suspended') {
      this.audioCtx.resume();
    }
  }

  playClickSound() {
    if (!this.soundEnabled || !this.audioCtx) return;
    this.ensureAudioContext();
    const osc = this.audioCtx.createOscillator();
    const gain = this.audioCtx.createGain();

    osc.type = 'sine';
    osc.frequency.setValueAtTime(440, this.audioCtx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(880, this.audioCtx.currentTime + 0.06);

    gain.gain.setValueAtTime(0.1, this.audioCtx.currentTime);
    gain.gain.exponentialRampToValueAtTime(0.01, this.audioCtx.currentTime + 0.06);

    osc.connect(gain);
    gain.connect(this.audioCtx.destination);

    osc.start();
    osc.stop(this.audioCtx.currentTime + 0.06);
  }

  playWinSound() {
    if (!this.soundEnabled || !this.audioCtx) return;
    this.ensureAudioContext();
    const notes = [523.25, 659.25, 783.99, 1046.50];
    notes.forEach((freq, idx) => {
      const osc = this.audioCtx.createOscillator();
      const gain = this.audioCtx.createGain();

      osc.type = 'triangle';
      osc.frequency.value = freq;

      const startTime = this.audioCtx.currentTime + idx * 0.08;
      gain.gain.setValueAtTime(0, startTime);
      gain.gain.linearRampToValueAtTime(0.15, startTime + 0.02);
      gain.gain.exponentialRampToValueAtTime(0.001, startTime + 0.3);

      osc.connect(gain);
      gain.connect(this.audioCtx.destination);

      osc.start(startTime);
      osc.stop(startTime + 0.3);
    });
  }

  /* ==========================================================================
     DOM & Event Listeners
     ========================================================================== */
  initDOM() {
    // Sound Button
    const soundBtn = document.getElementById('btn-sound');
    if (soundBtn) {
      soundBtn.textContent = this.soundEnabled ? 'Sound: On' : 'Sound: Off';
      soundBtn.addEventListener('click', () => {
        this.soundEnabled = !this.soundEnabled;
        localStorage.setItem('puzzle_sound', this.soundEnabled);
        soundBtn.textContent = this.soundEnabled ? 'Sound: On' : 'Sound: Off';
        this.showToast(this.soundEnabled ? 'Sound enabled' : 'Sound muted');
      });
    }

    // Shuffle Button
    const shuffleBtn = document.getElementById('btn-shuffle');
    if (shuffleBtn) {
      shuffleBtn.addEventListener('click', () => this.shuffle());
    }

    // Number Toggle Button
    const numbersBtn = document.getElementById('btn-numbers');
    if (numbersBtn) {
      numbersBtn.addEventListener('click', () => {
        this.showNumbers = !this.showNumbers;
        if (this.boardEl) {
          this.boardEl.classList.toggle('show-numbers', this.showNumbers);
        }
        numbersBtn.textContent = this.showNumbers ? 'Hide Numbers' : 'Show Numbers';
      });
    }

    // Hint Button
    const hintBtn = document.getElementById('btn-hint');
    if (hintBtn && this.ghostOverlay) {
      const activateHint = () => this.ghostOverlay.classList.add('active');
      const deactivateHint = () => this.ghostOverlay.classList.remove('active');

      hintBtn.addEventListener('mousedown', activateHint);
      hintBtn.addEventListener('mouseup', deactivateHint);
      hintBtn.addEventListener('mouseleave', deactivateHint);
      hintBtn.addEventListener('touchstart', activateHint, { passive: true });
      hintBtn.addEventListener('touchend', deactivateHint, { passive: true });
    }

    // Difficulty Selector
    const difficultySelect = document.getElementById('difficulty-select');
    if (difficultySelect) {
      difficultySelect.value = this.state.difficulty || 'medium';
      difficultySelect.addEventListener('change', (e) => {
        this.shuffle(e.target.value);
      });
    }
  }

  /* ==========================================================================
     Keyboard Controls (Arrow Keys & WASD)
     ========================================================================== */
  initKeyboard() {
    window.addEventListener('keydown', (e) => {
      if (['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement.tagName)) return;

      const blankIndex = this.state.board.indexOf(9);
      if (blankIndex === -1 || this.state.is_solved) return;

      const blankRow = Math.floor(blankIndex / 3);
      const blankCol = blankIndex % 3;
      let targetIndex = -1;

      switch (e.key) {
        case 'ArrowUp':
        case 'w':
        case 'W':
          if (blankRow < 2) targetIndex = (blankRow + 1) * 3 + blankCol;
          break;
        case 'ArrowDown':
        case 's':
        case 'S':
          if (blankRow > 0) targetIndex = (blankRow - 1) * 3 + blankCol;
          break;
        case 'ArrowLeft':
        case 'd':
        case 'D':
          if (blankCol < 2) targetIndex = blankRow * 3 + (blankCol + 1);
          break;
        case 'ArrowRight':
        case 'a':
        case 'A':
          if (blankCol > 0) targetIndex = blankRow * 3 + (blankCol - 1);
          break;
      }

      if (targetIndex !== -1) {
        e.preventDefault();
        this.moveTile(targetIndex);
      }
    });
  }

  /* ==========================================================================
     Mobile Touch Gestures (Swipe Detection)
     ========================================================================== */
  initTouch() {
    if (!this.boardContainer) return;

    let touchStartX = 0;
    let touchStartY = 0;

    this.boardContainer.addEventListener('touchstart', (e) => {
      if (e.touches.length === 1) {
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
      }
    }, { passive: true });

    this.boardContainer.addEventListener('touchend', (e) => {
      if (this.state.is_solved || !e.changedTouches.length) return;

      const touchEndX = e.changedTouches[0].clientX;
      const touchEndY = e.changedTouches[0].clientY;

      const deltaX = touchEndX - touchStartX;
      const deltaY = touchEndY - touchStartY;
      const threshold = 30;

      if (Math.abs(deltaX) < threshold && Math.abs(deltaY) < threshold) return;

      const blankIndex = this.state.board.indexOf(9);
      if (blankIndex === -1) return;

      const blankRow = Math.floor(blankIndex / 3);
      const blankCol = blankIndex % 3;
      let targetIndex = -1;

      if (Math.abs(deltaX) > Math.abs(deltaY)) {
        if (deltaX > 0) {
          if (blankCol > 0) targetIndex = blankRow * 3 + (blankCol - 1);
        } else {
          if (blankCol < 2) targetIndex = blankRow * 3 + (blankCol + 1);
        }
      } else {
        if (deltaY > 0) {
          if (blankRow > 0) targetIndex = (blankRow - 1) * 3 + blankCol;
        } else {
          if (blankRow < 2) targetIndex = (blankRow + 1) * 3 + blankCol;
        }
      }

      if (targetIndex !== -1) {
        this.moveTile(targetIndex);
      }
    }, { passive: true });
  }

  /* ==========================================================================
     Timer
     ========================================================================== */
  startTimer() {
    this.stopTimer();
    this.secondsElapsed = 0;
    this.updateTimerDisplay();
    this.isTimerRunning = true;
    this.timerInterval = setInterval(() => {
      if (this.isTimerRunning && !this.state.is_solved) {
        this.secondsElapsed++;
        this.updateTimerDisplay();
      }
    }, 1000);
  }

  stopTimer() {
    if (this.timerInterval) {
      clearInterval(this.timerInterval);
      this.timerInterval = null;
    }
    this.isTimerRunning = false;
  }

  updateTimerDisplay() {
    if (!this.timerEl) return;
    const mins = Math.floor(this.secondsElapsed / 60).toString().padStart(2, '0');
    const secs = (this.secondsElapsed % 60).toString().padStart(2, '0');
    this.timerEl.textContent = `${mins}:${secs}`;
  }

  /* ==========================================================================
     Board Rendering & Dynamic CSS Sprite Positioning
     ========================================================================== */
  render() {
    if (!this.boardEl) return;

    if (this.movesEl) this.movesEl.textContent = this.state.moves;
    if (this.hintImgEl) this.hintImgEl.src = this.state.image_url;
    if (this.hintTitleEl) this.hintTitleEl.textContent = this.state.image_title || 'Visual Target';
    if (this.ghostOverlay) {
      this.ghostOverlay.style.backgroundImage = `url('${this.state.image_url}')`;
    }

    if (this.difficultyBadge) {
      if (this.state.is_custom) {
        this.difficultyBadge.textContent = 'Custom';
      } else {
        this.difficultyBadge.textContent = (this.state.difficulty || 'medium').toUpperCase();
      }
    }

    const blankIndex = this.state.board.indexOf(9);
    const adjacentIndices = this.getAdjacentIndices(blankIndex);

    this.boardEl.innerHTML = '';

    this.state.board.forEach((val, idx) => {
      const tile = document.createElement('div');
      tile.className = 'puzzle-tile';
      tile.dataset.index = idx;
      tile.dataset.value = val;

      const isBlank = val === 9 && !this.state.is_solved;

      if (isBlank) {
        tile.classList.add('blank');
      } else {
        const origVal = val - 1;
        const origRow = Math.floor(origVal / 3);
        const origCol = origVal % 3;
        const posX = origCol * 50;
        const posY = origRow * 50;

        tile.style.backgroundImage = `url('${this.state.image_url}')`;
        tile.style.backgroundPosition = `${posX}% ${posY}%`;

        const numLabel = document.createElement('span');
        numLabel.className = 'tile-number';
        numLabel.textContent = val;
        tile.appendChild(numLabel);

        if (adjacentIndices.includes(idx) && !this.state.is_solved) {
          tile.classList.add('moveable');
          tile.addEventListener('click', () => this.moveTile(idx));
        }
      }

      this.boardEl.appendChild(tile);
    });

    if (this.state.is_solved) {
      this.triggerVictory();
    }
  }

  getAdjacentIndices(index) {
    if (index === -1) return [];
    const row = Math.floor(index / 3);
    const col = index % 3;
    const neighbors = [];
    if (row > 0) neighbors.push((row - 1) * 3 + col);
    if (row < 2) neighbors.push((row + 1) * 3 + col);
    if (col > 0) neighbors.push(row * 3 + (col - 1));
    if (col < 2) neighbors.push(row * 3 + (col + 1));
    return neighbors;
  }

  /* ==========================================================================
     Tile Movement & Backend Sync
     ========================================================================== */
  async moveTile(tileIndex) {
    if (this.state.is_solved || this.isProcessingMove) return;

    const blankIndex = this.state.board.indexOf(9);
    if (!this.getAdjacentIndices(blankIndex).includes(tileIndex)) {
      return;
    }

    this.isProcessingMove = true;
    this.playClickSound();

    const previousBoard = [...this.state.board];
    const previousMoves = this.state.moves;

    const newBoard = [...this.state.board];
    newBoard[blankIndex] = newBoard[tileIndex];
    newBoard[tileIndex] = 9;

    this.state.board = newBoard;
    this.state.moves++;
    this.state.is_solved = this.checkSolved(newBoard);

    this.render();

    try {
      const response = await fetch('/api/move/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': this.getCSRFToken(),
        },
        body: JSON.stringify({ tile_index: tileIndex }),
      });

      const data = await response.json();
      if (data.success) {
        this.state.board = data.board;
        this.state.moves = data.moves;
        this.state.is_solved = data.is_solved;
        this.render();
      } else {
        this.state.board = previousBoard;
        this.state.moves = previousMoves;
        this.state.is_solved = false;
        this.render();
      }
    } catch (err) {
      console.error('Move error:', err);
    } finally {
      this.isProcessingMove = false;
    }
  }

  checkSolved(board) {
    return board.every((val, idx) => val === idx + 1);
  }

  /* ==========================================================================
     Shuffle
     ========================================================================== */
  async shuffle(difficulty) {
    const diff = difficulty || this.state.difficulty || 'medium';
    try {
      const formData = new FormData();
      formData.append('difficulty', diff);

      const response = await fetch('/api/shuffle/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': this.getCSRFToken(),
        },
        body: formData,
      });

      const data = await response.json();
      if (data.success) {
        this.state.board = data.board;
        this.state.moves = 0;
        this.state.is_solved = false;
        this.state.difficulty = diff;
        this.startTimer();
        this.render();
        this.hideVictoryModal();
        this.showToast('Puzzle scrambled');
      }
    } catch (err) {
      console.error('Shuffle error:', err);
    }
  }

  /* ==========================================================================
     Victory Modal & Confetti
     ========================================================================== */
  triggerVictory() {
    this.stopTimer();
    this.playWinSound();

    const victoryModal = document.getElementById('victory-modal');
    const winMovesEl = document.getElementById('win-moves');
    const winTimeEl = document.getElementById('win-time');

    if (winMovesEl) winMovesEl.textContent = this.state.moves;
    if (winTimeEl) {
      const mins = Math.floor(this.secondsElapsed / 60);
      const secs = this.secondsElapsed % 60;
      winTimeEl.textContent = `${mins}m ${secs}s`;
    }

    if (victoryModal) {
      victoryModal.classList.add('active');
    }

    this.runConfetti();
  }

  hideVictoryModal() {
    const victoryModal = document.getElementById('victory-modal');
    if (victoryModal) victoryModal.classList.remove('active');
  }

  runConfetti() {
    const canvas = document.getElementById('confetti-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const particles = [];
    const colors = ['#0284c7', '#059669', '#d97706', '#6366f1', '#e11d48'];

    for (let i = 0; i < 90; i++) {
      particles.push({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height - canvas.height,
        r: Math.random() * 6 + 3,
        d: Math.random() * 30 + 10,
        color: colors[Math.floor(Math.random() * colors.length)],
        tilt: Math.floor(Math.random() * 10) - 10,
        tiltAngle: 0,
        tiltAngleInc: Math.random() * 0.06 + 0.03,
      });
    }

    let frameCount = 0;
    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      frameCount++;

      particles.forEach((p) => {
        p.tiltAngle += p.tiltAngleInc;
        p.y += (Math.cos(p.d) + 3 + p.r / 2) / 2;
        p.tilt = Math.sin(p.tiltAngle) * 12;

        ctx.beginPath();
        ctx.lineWidth = p.r / 2;
        ctx.strokeStyle = p.color;
        ctx.moveTo(p.x + p.tilt + p.r / 4, p.y);
        ctx.lineTo(p.x + p.tilt, p.y + p.tilt + p.r / 4);
        ctx.stroke();

        if (p.y > canvas.height) {
          p.x = Math.random() * canvas.width;
          p.y = -20;
        }
      });

      if (frameCount < 240) {
        requestAnimationFrame(draw);
      } else {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
      }
    };

    draw();
  }

  /* ==========================================================================
     Custom Photo Upload & Modals
     ========================================================================== */
  initModals() {
    const uploadBtn = document.getElementById('btn-upload-photo');
    const uploadModal = document.getElementById('upload-modal');
    const closeUploadBtn = document.getElementById('close-upload-modal');
    const dropzone = document.getElementById('upload-dropzone');
    const fileInput = document.getElementById('photo-input');
    const uploadForm = document.getElementById('upload-form');
    const previewContainer = document.getElementById('upload-preview-container');
    const previewImg = document.getElementById('upload-preview-img');
    const submitBtn = document.getElementById('btn-submit-upload');

    if (uploadBtn && uploadModal) {
      uploadBtn.addEventListener('click', () => uploadModal.classList.add('active'));
    }

    if (closeUploadBtn && uploadModal) {
      closeUploadBtn.addEventListener('click', () => uploadModal.classList.remove('active'));
    }

    if (dropzone && fileInput) {
      dropzone.addEventListener('click', () => fileInput.click());

      ['dragenter', 'dragover'].forEach((eventName) => {
        dropzone.addEventListener(eventName, (e) => {
          e.preventDefault();
          dropzone.classList.add('dragover');
        });
      });

      ['dragleave', 'drop'].forEach((eventName) => {
        dropzone.addEventListener(eventName, (e) => {
          e.preventDefault();
          dropzone.classList.remove('dragover');
        });
      });

      dropzone.addEventListener('drop', (e) => {
        if (e.dataTransfer.files.length) {
          fileInput.files = e.dataTransfer.files;
          this.handleFileSelected(e.dataTransfer.files[0], previewContainer, previewImg, submitBtn);
        }
      });

      fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) {
          this.handleFileSelected(e.target.files[0], previewContainer, previewImg, submitBtn);
        }
      });
    }

    if (uploadForm) {
      uploadForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        if (!fileInput.files.length) {
          this.showToast('Please select a photo first');
          return;
        }

        if (submitBtn) {
          submitBtn.disabled = true;
          submitBtn.textContent = 'Processing...';
        }

        const formData = new FormData();
        formData.append('photo', fileInput.files[0]);

        try {
          const response = await fetch('/api/upload-photo/', {
            method: 'POST',
            headers: {
              'X-CSRFToken': this.getCSRFToken(),
            },
            body: formData,
          });

          if (response.status === 413) {
            this.showToast('Image file is too large (Nginx max size exceeded)');
            return;
          }

          if (response.status === 403) {
            this.showToast('CSRF verification failed. Please refresh the page.');
            return;
          }

          let data;
          try {
            data = await response.json();
          } catch (e) {
            this.showToast('Server returned unexpected response');
            return;
          }

          if (data && data.success) {
            this.state.image_url = data.image_url;
            this.state.image_title = data.title;
            this.state.board = data.board;
            this.state.moves = 0;
            this.state.is_solved = false;
            this.state.is_custom = true;

            this.startTimer();
            this.render();
            if (uploadModal) uploadModal.classList.remove('active');
            this.showToast('Custom photo puzzle ready');
          } else {
            this.showToast((data && data.error) || 'Failed to upload image');
          }
        } catch (err) {
          console.error('Upload error:', err);
          this.showToast('Upload failed due to network error');
        } finally {
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Create Puzzle';
          }
        }
      });
    }

    const winPlayAgain = document.getElementById('win-btn-again');
    if (winPlayAgain) {
      winPlayAgain.addEventListener('click', () => {
        this.hideVictoryModal();
        this.shuffle();
      });
    }
  }

  handleFileSelected(file, previewContainer, previewImg, submitBtn) {
    if (!file.type.startsWith('image/')) {
      this.showToast('Please select an image file');
      return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
      if (previewImg && previewContainer) {
        previewImg.src = e.target.result;
        previewContainer.style.display = 'block';
      }
      if (submitBtn) submitBtn.disabled = false;
    };
    reader.readAsDataURL(file);
  }

  /* ==========================================================================
     Utilities
     ========================================================================== */
  getCSRFToken() {
    const cookieValue = document.cookie
      .split('; ')
      .find((row) => row.startsWith('csrftoken='))
      ?.split('=')[1];
    return cookieValue || '';
  }

  showToast(message) {
    let container = document.getElementById('toast-container');
    if (!container) {
      container = document.createElement('div');
      container.id = 'toast-container';
      container.className = 'toast-bar';
      document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = 'toast-msg';
    toast.textContent = message;

    container.appendChild(toast);
    setTimeout(() => {
      toast.style.opacity = '0';
      toast.style.transition = 'opacity 0.2s ease';
      setTimeout(() => toast.remove(), 200);
    }, 2200);
  }
}

// Instantiate on DOM load
document.addEventListener('DOMContentLoaded', () => {
  window.game = new PuzzleGame();
});
