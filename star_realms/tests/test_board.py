import unittest
import random

from ..board import Board

class TestBoard(unittest.TestCase):
    def setUp(self):
        random.seed(0)
        deck_path = 'star_realms/server/tests/input/test_game.json'
        self.board = Board(2, deck_path, deck_path)

    def test_next_turn(self):
        players = self.board.players
        self.assertEqual(self.board.get_current_player(), players[0])
        self.board.next_turn()
        self.assertEqual(self.board.get_current_player(), players[1])
        self.board.next_turn()
        self.assertEqual(self.board.get_current_player(), players[0])
