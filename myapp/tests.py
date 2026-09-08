import io
import json
from PIL import Image
from django.test import TestCase, Client
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from myapp.utils import (
    SOLVED_BOARD,
    BLANK_TILE,
    is_solvable,
    get_inversion_count,
    can_move,
    execute_move,
    is_solved,
    generate_scrambled_board,
    get_adjacent_indices,
)


class PuzzleLogicTests(TestCase):
    def test_solved_board_solvability(self):
        self.assertTrue(is_solvable(SOLVED_BOARD))
        self.assertTrue(is_solved(SOLVED_BOARD))
        self.assertEqual(get_inversion_count(SOLVED_BOARD), 0)

    def test_unsolvable_board_detection(self):
        # Swapping two tiles in a solved board creates 1 inversion (odd -> unsolvable)
        unsolvable_board = [2, 1, 3, 4, 5, 6, 7, 8, 9]
        self.assertFalse(is_solvable(unsolvable_board))
        self.assertEqual(get_inversion_count(unsolvable_board), 1)

    def test_solvable_scramble_generator(self):
        for diff in ['easy', 'medium', 'hard']:
            board = generate_scrambled_board(diff)
            self.assertEqual(len(board), 9)
            self.assertEqual(sorted(board), [1, 2, 3, 4, 5, 6, 7, 8, 9])
            self.assertTrue(is_solvable(board), f"Generated {diff} board must be solvable")
            self.assertFalse(is_solved(board), f"Generated {diff} board must not start already solved")

    def test_adjacent_indices(self):
        # Corner: index 0 (top-left) has neighbors 1 (right) and 3 (down)
        self.assertEqual(sorted(get_adjacent_indices(0)), [1, 3])
        # Center: index 4 has neighbors 1, 3, 5, 7
        self.assertEqual(sorted(get_adjacent_indices(4)), [1, 3, 5, 7])
        # Bottom-right corner: index 8 has neighbors 5, 7
        self.assertEqual(sorted(get_adjacent_indices(8)), [5, 7])

    def test_move_execution(self):
        # Blank at index 8 (bottom-right)
        board = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        # Valid moves into blank at index 8: index 5 (above) and index 7 (left)
        self.assertTrue(can_move(board, 7))
        self.assertTrue(can_move(board, 5))
        self.assertFalse(can_move(board, 0)) # Far corner cannot move

        new_board, valid = execute_move(board, 7)
        self.assertTrue(valid)
        self.assertEqual(new_board[7], 9)
        self.assertEqual(new_board[8], 8)


class PuzzleViewApiTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_index_page_status_and_session(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('game_state', response.context)
        self.assertIn('puzzle_game', self.client.session)
        session_game = self.client.session['puzzle_game']
        self.assertEqual(len(session_game['board']), 9)
        self.assertEqual(session_game['moves'], 0)

    def test_choices_page(self):
        response = self.client.get(reverse('choices'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('presets', response.context)

    def test_api_state_endpoint(self):
        response = self.client.get(reverse('api_game_state'))
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertIn('state', data)

    def test_api_shuffle(self):
        response = self.client.post(reverse('api_shuffle'), {'difficulty': 'hard'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['moves'], 0)
        self.assertEqual(data['difficulty'], 'hard')
        self.assertEqual(len(data['board']), 9)

    def test_api_move_valid_and_invalid(self):
        # Initialize session with a known board
        session = self.client.session
        session['puzzle_game'] = {
            'board': [1, 2, 3, 4, 5, 6, 7, 8, 9],
            'moves': 0,
            'is_solved': True,
            'image_id': 7,
            'image_url': '/media/myapp/images/img7.png',
            'image_title': 'Sydney Opera House',
            'difficulty': 'medium',
            'is_custom': False,
        }
        session.save()

        # Blank is at index 8. Move index 7 (adjacent)
        response = self.client.post(
            reverse('api_move'),
            data=json.dumps({'tile_index': 7}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertEqual(data['moves'], 1)
        self.assertEqual(data['board'][8], 8)
        self.assertEqual(data['board'][7], 9)

        # Move non-adjacent index (e.g. index 0)
        response = self.client.post(
            reverse('api_move'),
            data=json.dumps({'tile_index': 0}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertFalse(data['success'])
        self.assertFalse(data['is_valid_move'])

    def test_api_custom_photo_upload(self):
        # Generate a dummy RGB test image in memory with Pillow
        img = Image.new('RGB', (300, 300), color=(73, 109, 137))
        buffer = io.BytesIO()
        img.save(buffer, format='JPEG')
        buffer.seek(0)

        uploaded = SimpleUploadedFile(
            name='test_custom.jpg',
            content=buffer.read(),
            content_type='image/jpeg'
        )

        response = self.client.post(
            reverse('api_upload_photo'),
            {'photo': uploaded},
            format='multipart'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertTrue(data['image_url'].startswith('/media/uploads/'))
        self.assertEqual(data['moves'], 0)
        self.assertEqual(len(data['board']), 9)
        self.assertTrue(self.client.session['puzzle_game']['is_custom'])
