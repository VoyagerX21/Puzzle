# 🧩 Django 8-Puzzle Game

## Project Description

Welcome to the **Puzzle Game** — an interactive and fun brain teaser built with Python and Django! 🧩✨

The game presents you with a classic 3x3 puzzle where 8 pieces are scrambled, and your goal is to rearrange them to complete the full image. To help you out, a **visual hint** is provided, so you can strategize your moves wisely. 🎯

What makes this puzzle even more exciting?

- **Choose Your Favorite Image:** Select from a collection of images to play with your preferred puzzle design. 🎨
- **Step Counter:** Challenge yourself to solve the puzzle in as few moves as possible! After completion, the game displays the exact number of steps you took. ⏱️📊
- **Responsive Design:** The UI adapts seamlessly to different screen sizes, giving you a smooth experience on both desktop and mobile devices. 📱💻

Whether you're looking for a quick mental workout or just some casual fun, this puzzle game is the perfect way to engage your brain and test your problem-solving skills. Dive in and enjoy the challenge!


---

## 🚀 Features

- 8-tile sliding puzzle with a blank space
- Visual hint to guide you
- Multiple image options to choose from
- Tracks your total steps to solve the puzzle
- Responsive UI for desktop and mobile

---

## 📷 Screenshots

<div style="display: flex; gap: 10px; justify-content: center;">
  <img src="https://drive.google.com/file/d/11B9knSENfBIQlxOh0_BCny2uLd7Ni6w5/view?usp=sharing" alt="Screenshot 1" style="height: 200px; width: 100%; max-width: 33%; object-fit: cover;">
  <img src="https://drive.google.com/file/d/1TXtWRmr5PX9QiZzl8eUgqCzmdJ3XoCfs/view?usp=sharing" alt="Screenshot 2" style="height: 200px; width: 100%; max-width: 33%; object-fit: cover;">
  <img src="https://drive.google.com/file/d/14szxqVQdMSMe4Tw89QCmg1r0hN4DioS_/view?usp=sharing" alt="Screenshot 3" style="height: 200px; width: 100%; max-width: 33%; object-fit: cover;">
</div>

## 🔧 Installation

### 1. Clone the repository

```bash
git clone https://github.com/VoyagerX21/Puzzle.git
cd Puzzle
```

### 2. Create a virtual environment

```bash
python -m venv env
```

### 3. Activate the virtual enviornment

```bash
# for windows
.\env\Scripts\activate

# for macOS/Linux
source env/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Run the development server

```bash
python manage.py runserver
```

---

## 🧠 How to Play

1. Select your favorite image from the options.
2. Start the puzzle and slide the tiles to match the hint image.
3. Complete the puzzle in the least number of steps!

---

## 📂 Project Structure

```bash
your-project/
├── puzzle/             
├── media/myapp/             
├── myapp/         
├── manage.py             
├── db.sqlite3             
├── favicon.icon             
├── requirements.txt             
└── vercel.json
```

---
## Credits

Special thanks to **[Kunal-rawat](https://github.com/Kunal-Rawat007)** for designing and implementing the frontend of this project. Your creativity and effort made the game visually appealing and user-friendly! 🙌🎨

---

## 🙌 Contributions

Feel free to fork this repo and open a pull request to contribute!
