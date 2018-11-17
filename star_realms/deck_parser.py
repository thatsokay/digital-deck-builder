import json

from .card import Ship, Base

class ParseError(Exception):
    """
    Error while parsing a json file into a Deck.
    """
    def __init__(self, message):
        super().__init__(message)

def parse_deck(filename):
    """
    Same as parse_predefined_deck but returns a list of Cards.
    """
    with open(filename) as f:
        predefined = json.load(f)

    cards = []
    for prototype in predefined:
        quantity = prototype.get('quantity')
        if type(quantity) is not int:
            raise ParseError('Parsed non-integer quantity')

        card_data = prototype.get('card')
        if not card_data:
            raise ParseError('Card data not found')

        card_type = card_data.get('card_type')
        if card_type == 'Ship':
            for _ in range(quantity):
                cards.append(Ship(card_data))
        elif card_type == 'Base':
            for _ in range(quantity):
                cards.append(Base(card_data))
        else:
            raise ParseError('Card type not recognised')

    return cards
