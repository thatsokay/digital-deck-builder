class Card(object):
    def __init__(self, data):
        self.name = data['name']
        self.color = data['color']
        self.cost = data['cost']
        self.abilities = data['abilities']

    def __getitem__(self, key):
        return self.__getattribute__(key)

    def dump(self):
        return {
            'name': self.name,
            'color': self.color,
            'cost': self.cost,
            'abilities': self.abilities,
        }
