import unittest
import random
import socket
import os
from threading import Thread

from ..game import Game
from ..deck_parser import parse_deck

class TestGame(unittest.TestCase):
    def setUp(self):
        random.seed(0)
        file_dir = os.path.dirname(os.path.abspath(__file__))
        deck_dir = os.path.join(file_dir, 'input/test_game.json')
        self.game = Game(deck_dir, deck_dir)
        self.deck = parse_deck(deck_dir)

    def tearDown(self):
        self.game.close_connections()

    def test_init(self):
        expected_hands = [
            [
                self.deck[7],
                self.deck[8],
                self.deck[1],
            ],
            [
                self.deck[9],
                self.deck[4],
                self.deck[8],
                self.deck[6],
                self.deck[0],
            ],
        ]
        self.assertEqual(self.game.board.players[0].hand, expected_hands[0])
        self.assertEqual(self.game.board.players[1].hand, expected_hands[1])

    def test_game_end(self):
        self.game.board.players[0].objectives['authority'] = 0
        self.assertEqual(self.game.check_game_end(), True)

    def test_winners(self):
        self.assertEqual(self.game.get_winners(), self.game.board.players)

        self.game.board.players[0].objectives['authority'] = 0
        self.assertEqual(self.game.get_winners(), [self.game.board.players[1]])

    def test_connect_players(self):
        server_thread = Thread(target=self.game.connect_players)
        server_thread.start()

        for _ in range(2):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((socket.gethostname(), 4801))
            self.assertTrue(sock.recv(1024))
            sock.close()

        server_thread.join(1)
        self.assertFalse(server_thread.is_alive())
        self.assertEqual(len(self.game.connections), 2)

    def test_game_start(self):
        server_thread = Thread(target=self.game.connect_players)
        server_thread.start()

        players = []
        for _ in range(2):
            player = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            player.connect((socket.gethostname(), 4801))
            players.append(player)

        server_thread.join(1)
        self.assertFalse(server_thread.is_alive())

        game_thread = Thread(target=self.game.start)
        game_thread.start()

        players[0].send(b'{"action": "quit"}\n')

        game_thread.join(1)
        self.assertFalse(server_thread.is_alive())

        for player in players:
            player.close()
