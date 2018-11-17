from random import shuffle, choice

from .deck_parser import parse_deck
from .player import Player

class Board(object):
    def __init__(self, num_players, start_deck, trade_deck):
        if num_players < 2:
            raise ValueError('Cannot create game with less than 2 players')
        self.num_players = num_players
        self.current_turn = 0

        self.players = []
        deck = parse_deck(start_deck)
        for i in range(self.num_players):
            player = Player(list(deck))
            if i == 0:
                player.draw(3)
            else:
                player.draw(4)
            self.players.append(player)

        trade_deck = parse_deck(trade_deck)
        shuffle(trade_deck)
        self.trade_row = tuple(trade_deck[:5] + [None for _ in range(5 - len(trade_deck))])
        self.trade_deck = trade_deck[len(self.trade_row):]
        self.trash_pile = []

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
        player.draw(4)

        if len(player.discard_pile):
            discard = choice(player.discard_pile)
            player.discard_pile.remove(discard)
        elif len(player.draw_pile):
            discard = choice(player.draw_pile)
            player.draw_pile.remove(discard)
        elif len(player.hand):
            discard = choice(player.hand)
            player.hand.remove(discard)

        self.current_turn = (self.current_turn + 1) % self.num_players

    def game_over(self):
        return 0 in [
            len(player.hand) + len(player.draw_pile) + len(player.discard_pile) + len(player.in_play)
            for player in self.players
        ]