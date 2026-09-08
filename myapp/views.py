import json
import time
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie

from .utils import (
    PRESETS,
    PRESET_DICT,
    BLANK_TILE,
    SOLVED_BOARD,
    get_preset_by_id,
    is_solvable,
    can_move,
    execute_move,
    is_solved,
    generate_scrambled_board,
    process_and_save_upload,
)
from .forms import PhotoUploadForm


def get_or_init_game_state(request):
    """
    Retrieve current game state from Django session or initialize fresh state.
    Guarantees full isolation between different user sessions without globals.
    """
    game = request.session.get('puzzle_game')
    
    if not game or 'board' not in game:
        default_preset = PRESETS[0]
        initial_board = generate_scrambled_board('medium')
        game = {
            'board': initial_board,
            'moves': 0,
            'is_solved': False,
            'difficulty': 'medium',
            'image_id': default_preset['id'],
            'image_url': default_preset['image_url'],
            'image_title': default_preset['title'],
            'is_custom': False,
            'start_time': int(time.time()),
        }
        request.session['puzzle_game'] = game
        request.session.modified = True

    return game


@ensure_csrf_cookie
def index(request):
    """
    Main Game View:
    Renders the modern SPA-like puzzle dashboard with initial state pre-populated.
    """
    game = get_or_init_game_state(request)
    context = {
        'game_state': game,
        'game_state_json': json.dumps(game),
        'presets': PRESETS,
        'presets_json': json.dumps(PRESETS),
    }
    return render(request, 'myapp/index.html', context)


@ensure_csrf_cookie
def choices(request):
    """
    Gallery / Image Picker View:
    Displays catalog of all 16 presets + custom upload trigger.
    """
    game = get_or_init_game_state(request)
    context = {
        'presets': PRESETS,
        'current_image_id': game.get('image_id'),
        'current_image_url': game.get('image_url'),
    }
    return render(request, 'myapp/choice.html', context)


@require_GET
def api_game_state(request):
    """Return current game state as JSON."""
    game = get_or_init_game_state(request)
    return JsonResponse({'success': True, 'state': game})


@require_POST
def api_move(request):
    """
    Execute a tile move:
    Validates tile adjacency to blank space, updates board & moves in session,
    and returns updated state.
    """
    game = get_or_init_game_state(request)
    
    # Parse tile_index from JSON payload or form data
    tile_index = None
    if request.content_type == 'application/json':
        try:
            body = json.loads(request.body)
            tile_index = body.get('tile_index')
        except (ValueError, TypeError):
            return HttpResponseBadRequest("Invalid JSON body")
    else:
        tile_index = request.POST.get('tile_index')

    if tile_index is None:
        return JsonResponse({'success': False, 'error': 'Missing tile_index'}, status=400)

    try:
        tile_index = int(tile_index)
    except ValueError:
        return JsonResponse({'success': False, 'error': 'tile_index must be an integer'}, status=400)

    board = game.get('board', list(SOLVED_BOARD))
    if not can_move(board, tile_index):
        return JsonResponse({
            'success': False,
            'is_valid_move': False,
            'error': 'Tile cannot be moved into blank position.',
            'board': board,
            'moves': game.get('moves', 0),
            'is_solved': game.get('is_solved', False),
        })

    new_board, valid = execute_move(board, tile_index)
    new_moves = game.get('moves', 0) + 1
    won = is_solved(new_board)

    game['board'] = new_board
    game['moves'] = new_moves
    game['is_solved'] = won

    request.session['puzzle_game'] = game
    request.session.modified = True

    return JsonResponse({
        'success': True,
        'is_valid_move': True,
        'board': new_board,
        'moves': new_moves,
        'is_solved': won,
    })


@require_POST
def api_shuffle(request):
    """
    Scramble the board with a guaranteed solvable configuration,
    reset move counter and timer.
    """
    game = get_or_init_game_state(request)
    difficulty = request.POST.get('difficulty', game.get('difficulty', 'medium'))

    new_board = generate_scrambled_board(difficulty)
    game['board'] = new_board
    game['moves'] = 0
    game['is_solved'] = False
    game['difficulty'] = difficulty
    game['start_time'] = int(time.time())

    request.session['puzzle_game'] = game
    request.session.modified = True

    return JsonResponse({
        'success': True,
        'board': new_board,
        'moves': 0,
        'is_solved': False,
        'difficulty': difficulty,
    })


@require_POST
def api_select_preset(request):
    """
    Select a preset image by ID, scramble new board, and update session.
    """
    try:
        preset_id = int(request.POST.get('id', 7))
    except (ValueError, TypeError):
        preset_id = 7

    preset = get_preset_by_id(preset_id)
    game = get_or_init_game_state(request)

    game['image_id'] = preset['id']
    game['image_url'] = preset['image_url']
    game['image_title'] = preset['title']
    game['is_custom'] = False
    game['board'] = generate_scrambled_board(game.get('difficulty', 'medium'))
    game['moves'] = 0
    game['is_solved'] = False
    game['start_time'] = int(time.time())

    request.session['puzzle_game'] = game
    request.session.modified = True

    # If it was an AJAX call, return JSON, else redirect to main game
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.content_type == 'application/json':
        return JsonResponse({'success': True, 'state': game})

    return redirect('index')


@require_POST
def api_upload_photo(request):
    """
    Handle user custom photo upload:
    Validates file format/size with Django Form, processes with Pillow,
    and sets as active game image.
    """
    form = PhotoUploadForm(request.POST, request.FILES)
    if not form.is_valid():
        error_msg = next(iter(form.errors.values()))[0] if form.errors else "Invalid upload."
        return JsonResponse({'success': False, 'error': error_msg}, status=400)

    photo = form.cleaned_data['photo']
    try:
        result = process_and_save_upload(photo, session_key=request.session.session_key)
    except Exception as e:
        return JsonResponse({'success': False, 'error': f"Failed to process image: {str(e)}"}, status=500)

    game = get_or_init_game_state(request)
    game['image_id'] = None
    game['image_url'] = result['image_url']
    game['image_title'] = result['title']
    game['is_custom'] = True
    game['board'] = generate_scrambled_board(game.get('difficulty', 'medium'))
    game['moves'] = 0
    game['is_solved'] = False
    game['start_time'] = int(time.time())

    request.session['puzzle_game'] = game
    request.session.modified = True

    return JsonResponse({
        'success': True,
        'image_url': result['image_url'],
        'title': result['title'],
        'board': game['board'],
        'moves': 0,
        'is_solved': False,
    })


@require_POST
def api_reset(request):
    """Reset the current game board to a freshly shuffled solvable state."""
    return api_shuffle(request)
