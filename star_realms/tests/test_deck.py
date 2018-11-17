import unittest

from ..card import Card
from ..deck import Deck

class TestDeck(unittest.TestCase):
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
        self.deck = Deck(list(self.cards)) # Use copy of cards

    def test_deal(self):
        top_card = self.cards[0]
        self.assertEqual(self.deck.deal(), top_card)

    def test_subdeck(self):
        top_cards = self.cards[:3]
        self.assertEqual(self.deck.subdeck(3), top_cards)

    def test_subdeck_entire(self):
        cards = self.cards
        self.assertEqual(self.deck.subdeck(9), cards)
