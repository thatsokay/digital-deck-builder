from random import shuffle

from .card import Base

class Player(object):
    """
    Represents a player. Stores a player's draw and discard piles, hand, and
    resources.
    """
    def __init__(self, deck=[]):
        """
        Initialises the player's deck and hand.

        Args:
            deck: The player's starting deck. Defaults to an empty list.
        """
        self.draw_pile = deck
        self.discard_pile = []
        self.hand = []
        self.in_play = []
        self.objectives = {
            'authority': 50
        }
        self.resources = {
            'trade': 0,
            'combat': 0
        }
        self.used_ally_ability = []

        shuffle(self.draw_pile)

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def dump(self):
        return {
            'draw_pile': [card.dump() for card in self.draw_pile],
            'discard_pile': [card.dump() for card in self.discard_pile],
            'hand': [card.dump() for card in self.hand],
            'in_play': [card.dump() for card in self.in_play],
            'objectives': self.objectives,
            'resources': self.resources,
        }

    def play_card(self, index):
        """
        Moves the card at the given index from the hand to in play and returns
        it.

        Args:
            index: Index of the card in hand to be played.

        Returns:
            The played card. Returns None if no card at the given index.
        """
        card = self.hand.pop(index)
        self.in_play.append(card)
        return card

    def discard_played(self):
        """
        Moves all the cards from in play to the discard pile.
        """
        self.discard_pile.extend(filter(lambda x: type(x) is not Base, self.in_play))
        self.in_play = list(filter(lambda x: type(x) is Base, self.in_play))

    def discard_hand(self):
        """
        Moves all the cards from the hand to the discard pile.
        """
        self.discard_pile.extend(self.hand)
        self.hand = []

    def draw(self, num):
        draw_remainder = len(self.draw_pile)
        self.hand.extend(self.draw_pile[:num])
        self.draw_pile = self.draw_pile[num:]
        if draw_remainder < num:
            self.cycle_deck()
            self.hand.extend(self.draw_pile[:num - draw_remainder])
            self.draw_pile = self.draw_pile[num - draw_remainder:]

    def cycle_deck(self):
        """
        Shuffle the discard pile, replace the draw pile with it, and empty
        the discard pile.
        """
        shuffle(self.discard_pile)
        self.draw_pile = self.discard_pile
        self.discard_pile = []

    def add_objective(self, objective, amount):
        """
        Increase a player objective by the given amount. Player resources cannot
        be reduced below zero. Returns the new value of the affected objective
        or None if the given objective doesn't exist.
        """
        if self.objectives.get(objective) is None:
            raise ValueError('{} is not a objective'.format(objective))
        if self.objectives.get(objective) < -amount:
            self.objectives[objective] = 0
        else:
            self.objectives[objective] += amount
        return self.objectives.get(objective)

    def add_resource(self, resource, amount):
        """
        Increase a player resource by the given amount. Player resources cannot
        be reduced below zero. Returns the new value of the affected resource or
        None if the given resource doesn't exist.
        """
        if self.resources.get(resource) is None:
            raise ValueError('{} is not a resource'.format(resource))
        if self.resources.get(resource) < -amount:
            self.resources[resource] = 0
        else:
            self.resources[resource] += amount
        return self.resources.get(resource)

    def reset_resources(self):
        """
        Sets all of the player's resources to zero.
        """
        for resource in self.resources.keys():
            self.resources[resource] = 0
