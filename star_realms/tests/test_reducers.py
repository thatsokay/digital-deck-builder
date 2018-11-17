import unittest
import random
import os

from ..  import reducers
from ..deck_parser import parse_deck
from ..board import Board

class TestReducers(unittest.TestCase):
    def setUp(self):
        random.seed(0)
        file_dir = os.path.dirname(os.path.abspath(__file__))
        deck_dir = os.path.join(file_dir, 'input/test_game.json')
        self.board = Board(2, deck_dir, deck_dir)

    def test_end_turn(self):
        players = self.board.players
        self.assertEqual(self.board.get_current_player(), players[0])
        action = {'action': 'end_turn'}
        getattr(reducers, action['action'])(self.board, action)
        self.assertEqual(self.board.get_current_player(), players[1])

    def test_play_card(self):
        player = self.board.get_current_player()
        file_dir = os.path.dirname(os.path.abspath(__file__))
        deck_dir = os.path.join(file_dir, 'input/test_game.json')
        deck = parse_deck(deck_dir)
        action = {'action': 'play_card', 'hand_index': 0}
        getattr(reducers, action['action'])(self.board, action)
        self.assertEqual(player.in_play[0], deck[7])
