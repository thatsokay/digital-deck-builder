class Card(object):
    """
    Represents a single game card.
    """
    def __init__(self, data):
        self.name = data['name']
        self.faction = data.get('faction')
        self.cost = data.get('cost')
        self.abilities = data.get('abilities', {})

    def __str__(self):
        return 'Card({})'.format(self.name)

    def __repr__(self):
        return 'Card({})'.format(
            self.name.__repr__(),
        )

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def dump(self):
        return {
            'name': self.name,
            'card_type': self.__class__.__name__,
            'faction': self.faction,
            'cost': self.cost,
            'abilities': self.abilities,
        }


class Ship(Card):
    """
    Represents a ship card.
    """
    def __init__(self, data):
        Card.__init__(self, data) # TODO: Other attributes

    def __str__(self):
        return 'Ship({})'.format(self.name)

    def __repr__(self):
        return 'Ship({})'.format(
            self.name.__repr__(),
        )


class Base(Card):
    """
    Represents a ship card.
    """
    def __init__(self, data):
        Card.__init__(self, data) # TODO: Other attributes
        self.outpost = data['outpost']
        self.defense = data['defense']

    def __str__(self):
        return 'Base({})'.format(self.name)

    def __repr__(self):
        return 'Base({})'.format(
            self.name.__repr__(),
        )

    def dump(self):
        return {
            **super().dump(),
            'outpost': self.outpost,
            'defense': self.defense,
        }
