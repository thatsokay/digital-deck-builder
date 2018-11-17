import unittest
import json
import os

from ..card import Card

class TestCard(unittest.TestCase):
    def test_card(self):
        file_dir = os.path.dirname(os.path.abspath(__file__))
        deck_dir = os.path.join(file_dir, 'input/test_card.json')
        with open(deck_dir) as f:
            data = json.load(f)
        card = Card(data)

        self.assertEqual(card.name, 'name')

    def test_eq(self):
        data = {
            'name': 'name',
            'faction': 'faction',
            'cost': 1,
            'abilities': []
        }

        card1 = Card(data)
        card2 = Card(data)

        self.assertEqual(card1, card2)
