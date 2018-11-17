from random import shuffle

class Player(object):
    def __init__(self, deck=[]):
        self.draw_pile = deck
        self.discard_pile = []
        self.hand = []
        self.in_play = []
        self.resources = {
            'red': 0,
            'green': 0,
            'blue': 0,
            'yellow': 0,
        }

        shuffle(self.draw_pile)

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def dump(self):
        return {
            'draw_pile': [card.dump() for card in self.draw_pile],
            'discard_pile': [card.dump() for card in self.discard_pile],
            'hand': [card.dump() for card in self.hand],
            'in_play': [card.dump() for card in self.in_play],
            'resources': self.resources,
        }

    def draw(self, num):
        draw_remainder = len(self.draw_pile)
        self.hand.extend(self.draw_pile[:num])
        self.draw_pile = self.draw_pile[num:]
        if draw_remainder < num:
            # Cycle deck
            shuffle(self.discard_pile)
            self.draw_pile = self.discard_pile
            self.discard_pile = []
            # Draw
            self.hand.extend(self.draw_pile[:num - draw_remainder])
            self.draw_pile = self.draw_pile[num - draw_remainder:]

    def discard_played(self):
        self.discard_pile.extend(self.in_play)
        self.in_play = []

    def discard_hand(self):
        self.discard_pile.extend(self.hand)
        self.hand = []

    def reset_resources(self):
        for resources in self.resources.keys():
            self.resources[resources] = 0
