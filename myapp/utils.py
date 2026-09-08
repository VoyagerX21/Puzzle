import os
import random
import uuid
from pathlib import Path
from PIL import Image, ImageOps
from django.conf import settings

BLANK_TILE = 9
GRID_SIZE = 3
SOLVED_BOARD = [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Preset images catalog with curated metadata
PRESETS = [
    {
        'id': 7,
        'title': 'Sydney Opera House',
        'category': 'Landmark',
        'difficulty': 'Medium',
        'description': 'Iconic performing arts centre in Sydney Harbour with sail-shaped shells.',
        'image_url': '/media/myapp/images/img7.png',
    },
    {
        'id': 8,
        'title': 'Apple Park',
        'category': 'Campus',
        'difficulty': 'Easy',
        'description': 'Futuristic ring-shaped corporate headquarters in Cupertino, California.',
        'image_url': '/media/myapp/images/img8.png',
    },
    {
        'id': 9,
        'title': 'Taj Mahal',
        'category': 'Monument',
        'difficulty': 'Easy',
        'description': 'Magnificent ivory-white marble mausoleum on the right bank of the river Yamuna.',
        'image_url': '/media/myapp/images/img9.png',
    },
    {
        'id': 10,
        'title': 'Bhaktapur Durbar',
        'category': 'Heritage',
        'difficulty': 'Hard',
        'description': 'Ancient Newar city in the Kathmandu Valley, famous for intricate woodcraft.',
        'image_url': '/media/myapp/images/img10.png',
    },
    {
        'id': 11,
        'title': 'Petra Treasury',
        'category': 'Archaeological',
        'difficulty': 'Medium',
        'description': 'Rose-red historic city carved directly into sandstone cliffs in Jordan.',
        'image_url': '/media/myapp/images/img11.png',
    },
    {
        'id': 12,
        'title': 'Machu Picchu',
        'category': 'Ruins',
        'difficulty': 'Easy',
        'description': '15th-century Inca citadel set high in the Andes Mountains of Peru.',
        'image_url': '/media/myapp/images/img12.png',
    },
    {
        'id': 13,
        'title': 'Leaning Tower of Pisa',
        'category': 'Landmark',
        'difficulty': 'Hard',
        'description': 'World-famous freestanding bell tower known for its unintended tilt in Italy.',
        'image_url': '/media/myapp/images/img13.png',
    },
    {
        'id': 14,
        'title': 'Serene Monk',
        'category': 'Spiritual',
        'difficulty': 'Medium',
        'description': 'Peaceful scene of a monk in meditation surrounded by temple lanterns.',
        'image_url': '/media/myapp/images/img14.png',
    },
    {
        'id': 15,
        'title': 'Humpback Whale',
        'category': 'Wildlife',
        'difficulty': 'Easy',
        'description': 'Majestic ocean gentle giant leaping from the deep blue sea.',
        'image_url': '/media/myapp/images/img15.png',
    },
    {
        'id': 16,
        'title': 'Forest Campfire',
        'category': 'Outdoors',
        'difficulty': 'Medium',
        'description': 'Cozy illuminated tent under starry night skies in the wilderness.',
        'image_url': '/media/myapp/images/img16.png',
    },
    {
        'id': 1,
        'title': 'Eco Haven',
        'category': 'Scenery',
        'difficulty': 'Hard',
        'description': 'Vibrant tropical jungle with cascading waterfalls and morning sunbeams.',
        'image_url': '/media/myapp/images/img1.png',
    },
    {
        'id': 2,
        'title': 'Sunset Wheatfield',
        'category': 'Scenery',
        'difficulty': 'Hard',
        'description': 'Golden ripples of wheat glowing in the warmth of a countryside sunset.',
        'image_url': '/media/myapp/images/img2.png',
    },
    {
        'id': 3,
        'title': 'Bell Rock Sedona',
        'category': 'Nature',
        'difficulty': 'Medium',
        'description': 'Vivid red sandstone formation rising above the Arizona high desert.',
        'image_url': '/media/myapp/images/img3.png',
    },
    {
        'id': 4,
        'title': 'Ligurian Coast',
        'category': 'Seaside',
        'difficulty': 'Hard',
        'description': 'Pastel cliffside Italian villages meeting crystal clear Mediterranean waters.',
        'image_url': '/media/myapp/images/img4.png',
    },
    {
        'id': 5,
        'title': 'Tran Quoc Pagoda',
        'category': 'Temple',
        'difficulty': 'Hard',
        'description': 'Oldest Buddhist pagoda in Hanoi located on an island in West Lake.',
        'image_url': '/media/myapp/images/img5.png',
    },
    {
        'id': 6,
        'title': 'Notre-Dame Cathedral',
        'category': 'Cathedral',
        'difficulty': 'Medium',
        'description': 'Gothic masterpiece situated on Île de la Cité in Paris, France.',
        'image_url': '/media/myapp/images/img6.png',
    },
]

PRESET_DICT = {p['id']: p for p in PRESETS}


def get_preset_by_id(preset_id: int):
    """Retrieve a preset image dict by ID, defaulting to Sydney Opera House."""
    return PRESET_DICT.get(preset_id, PRESETS[0])


def get_inversion_count(board):
    """Calculate inversion count for 3x3 8-puzzle excluding blank tile 9."""
    inv_count = 0
    clean_arr = [x for x in board if x != BLANK_TILE]
    n = len(clean_arr)
    for i in range(n):
        for j in range(i + 1, n):
            if clean_arr[i] > clean_arr[j]:
                inv_count += 1
    return inv_count


def is_solvable(board):
    """
    In a standard 3x3 8-puzzle (odd grid width),
    a configuration is solvable if and only if inversion count is even.
    """
    return get_inversion_count(board) % 2 == 0


def get_adjacent_indices(index: int):
    """Return valid 0-8 adjacent indices (up, down, left, right) for a tile index."""
    row, col = index // GRID_SIZE, index % GRID_SIZE
    neighbors = []
    if row > 0:
        neighbors.append((row - 1) * GRID_SIZE + col)  # Up
    if row < GRID_SIZE - 1:
        neighbors.append((row + 1) * GRID_SIZE + col)  # Down
    if col > 0:
        neighbors.append(row * GRID_SIZE + (col - 1))  # Left
    if col < GRID_SIZE - 1:
        neighbors.append(row * GRID_SIZE + (col + 1))  # Right
    return neighbors


def can_move(board, tile_index: int) -> bool:
    """Check if the given tile index can slide into the blank space."""
    if tile_index < 0 or tile_index >= len(board):
        return False
    blank_index = board.index(BLANK_TILE)
    return tile_index in get_adjacent_indices(blank_index)


def execute_move(board, tile_index: int):
    """
    Execute move by swapping tile at tile_index with the blank tile.
    Returns (new_board, is_valid).
    """
    if not can_move(board, tile_index):
        return list(board), False

    new_board = list(board)
    blank_index = new_board.index(BLANK_TILE)
    new_board[blank_index], new_board[tile_index] = new_board[tile_index], new_board[blank_index]
    return new_board, True


def is_solved(board) -> bool:
    """Check if the board matches the solved state [1, 2, 3, 4, 5, 6, 7, 8, 9]."""
    return board == SOLVED_BOARD


def generate_scrambled_board(difficulty='medium'):
    """
    Generate a guaranteed-solvable scrambled board.
    Uses random walk from solved state to ensure natural solvable distribution
    and enforce difficulty levels if desired.
    """
    move_counts = {
        'easy': 20,
        'medium': 45,
        'hard': 90,
    }
    steps = move_counts.get(difficulty.lower(), 45)

    board = list(SOLVED_BOARD)
    last_blank = -1

    for _ in range(steps):
        blank_index = board.index(BLANK_TILE)
        neighbors = [idx for idx in get_adjacent_indices(blank_index) if idx != last_blank]
        if not neighbors:
            neighbors = get_adjacent_indices(blank_index)
        chosen = random.choice(neighbors)
        board[blank_index], board[chosen] = board[chosen], board[blank_index]
        last_blank = blank_index

    # If by chance it landed back on solved state, do a few extra moves
    while is_solved(board) or not is_solvable(board):
        blank_index = board.index(BLANK_TILE)
        chosen = random.choice(get_adjacent_indices(blank_index))
        board[blank_index], board[chosen] = board[chosen], board[blank_index]

    return board


def process_and_save_upload(uploaded_file, session_key: str = None) -> dict:
    """
    Process an uploaded image:
    1. Read with Pillow.
    2. Auto-orient via EXIF.
    3. Crop to 1:1 square centered.
    4. Resize to max 800x800 for optimal performance.
    5. Save safely to media/uploads/ directory.
    Returns dict with image_url, title, and relative path.
    """
    uploads_dir = Path(settings.MEDIA_ROOT) / 'uploads'
    uploads_dir.mkdir(parents=True, exist_ok=True)

    # Open image with Pillow
    img = Image.open(uploaded_file)
    img = ImageOps.exif_transpose(img)

    # Convert to RGB if palette/RGBA
    if img.mode in ('RGBA', 'LA', 'P'):
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')

    # Center square crop
    w, h = img.size
    min_dim = min(w, h)
    left = (w - min_dim) // 2
    top = (h - min_dim) // 2
    right = left + min_dim
    bottom = top + min_dim
    img_cropped = img.crop((left, top, right, bottom))

    # Resize if larger than 800x800
    if min_dim > 800:
        img_cropped = img_cropped.resize((800, 800), Image.Resampling.LANCZOS)

    # Unique file name
    file_id = uuid.uuid4().hex[:10]
    filename = f"custom_{file_id}.jpg"
    target_path = uploads_dir / filename

    img_cropped.save(target_path, 'JPEG', quality=92, optimize=True)

    image_url = f"{settings.MEDIA_URL}uploads/{filename}"
    original_name = Path(uploaded_file.name).stem.replace('_', ' ').replace('-', ' ').title()
    title = f"Custom: {original_name[:24]}" if original_name else "Custom Upload"

    return {
        'image_url': image_url,
        'title': title,
        'filename': filename,
    }
