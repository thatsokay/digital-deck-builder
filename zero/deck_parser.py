import json

from .card import Card

def parse_deck(filename):
    with open(filename) as f:
        deck = json.load(f)
    cards = []
    for spec in deck:
        quantity = spec['quantity']
        card_data = spec['card']
        for _ in range(quantity):
            cards.append(Card(card_data))
    return cards
