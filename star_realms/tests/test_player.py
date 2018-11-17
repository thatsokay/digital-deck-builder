import unittest

from ..player import Player
from ..card import Card

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.cards = []
        for i in range(4):
            data = {
                'name': str(i),
                'faction': str(i),
                'cost': i,
                'abilities': []
            }
            self.cards.append(Card(data))
        self.player = Player(self.cards)

    def test_draw(self):
        self.player.draw(2)

        self.assertEqual(len(self.player.hand), 2)
        self.assertEqual(len(self.player.draw_pile), 2)
        self.assertEqual(len(self.player.discard_pile), 0)

    def test_draw_all(self):
        self.player.draw(9)

        self.assertEqual(len(self.player.hand), 4)
        self.assertEqual(len(self.player.draw_pile), 0)
        self.assertEqual(len(self.player.discard_pile), 0)

    def test_discard_hand(self):
        self.player.draw(2)
        self.player.discard_hand()

        self.assertEqual(len(self.player.hand), 0)
        self.assertEqual(len(self.player.draw_pile), 2)
        self.assertEqual(len(self.player.discard_pile), 2)

    def test_cycle_deck(self):
        self.player.discard_pile = self.player.draw_pile
        self.player.draw_pile = []
        self.player.cycle_deck()

        self.assertEqual(len(self.player.hand), 0)
        self.assertEqual(len(self.player.draw_pile), 4)
        self.assertEqual(len(self.player.discard_pile), 0)

    def test_objective(self):
        self.player.add_objective('authority', 1)
        self.assertEqual(self.player.objectives['authority'], 51)

        self.player.add_objective('authority', -100)
        self.assertEqual(self.player.objectives['authority'], 0)

    def test_resource(self):
        self.player.add_resource('trade', 1)
        self.player.add_resource('combat', -1)

        self.assertEqual(self.player.resources['trade'], 1)
        self.assertEqual(self.player.resources['combat'], 0)

        self.player.reset_resources()

        self.assertEqual(self.player.resources['trade'], 0)
        self.assertEqual(self.player.resources['combat'], 0)

    def test_end_turn(self):
        self.player.discard_pile = self.player.draw_pile[:1]
        self.player.hand = self.player.draw_pile[1:3]
        self.player.draw_pile = self.player.draw_pile[3:]

        self.player.discard_hand()
        self.player.draw(3)

        self.assertEqual(len(self.player.discard_pile), 0)
        self.assertEqual(len(self.player.hand), 3)
        self.assertEqual(len(self.player.draw_pile), 1)
