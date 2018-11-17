from random import shuffle

from . import abilities
from .deck_parser import parse_deck
from .player import Player

class ChooseError(Exception):
    def __init__(self, choose):
        pass

class Board(object):
    """
    The state of the game.
    """
    def __init__(self, num_players, start_deck, trade_deck, explorer):
        """
        Initialises players and starting deck.

        Args:
            deck_path: String containing the filepath of the starting deck.
        """
        if num_players < 2:
            raise ValueError('Cannot create game with less than 2 players')
        self.num_players = num_players
        self.current_turn = 0

        self.players = []
        deck = parse_deck(start_deck)
        for i in range(self.num_players):
            player = Player(list(deck)) # Copy of start deck
            if i == 0:
                player.draw(3)
            else:
                player.draw(5)
            self.players.append(player)

        trade_deck = parse_deck(trade_deck)
        explorer = parse_deck(explorer)
        shuffle(trade_deck)
        self.trade_row = tuple(explorer + trade_deck[:5] + [None for _ in range(5 - len(trade_deck))])
        self.trade_deck = trade_deck[len(self.trade_row):]
        self.trash_pile = []
        self.pending_choices = []

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def dump(self):
        return {
            'num_players': self.num_players,
            'current_turn': self.current_turn,
            'players': [player.dump() for player in self.players],
            'trade_deck': [card.dump() for card in self.trade_deck],
            'trade_row': [card.dump() if card else None for card in self.trade_row],
            'trash_pile': [card.dump() for card in self.trash_pile],
        }

    def get_current_player(self):
        return self.players[self.current_turn]

    def next_turn(self):
        player = self.get_current_player()
        player.discard_played()
        player.discard_hand()
        player.reset_resources()
        player.used_ally_ability = []
        player.draw(5)
        self.current_turn = (self.current_turn + 1) % self.num_players

    def buy_card(self, index):
        if index > 0:
            card = self.trade_row[index]
            try:
                replacement = self.trade_deck.pop(0)
            except IndexError:
                replacement = None
            self.trade_row = self.trade_row[:index] + (replacement,) + self.trade_row[index + 1:]
            return card
        else:
            return self.trade_row[0]

    def game_over(self):
        return True in [player.objectives['authority'] <= 0 for player in self.players]
