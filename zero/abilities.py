from random import sample

def resource(state, card, player_num, **kwargs):
    player = state.players[player_num]
    for resource_type, amount in kwargs.items():
        player.resources[resource_type] += amount

def discard(state, card, player_num, **kwargs):
    opponent = state.players[(player_num + 1) % state.num_players]
    discards_left = kwargs['discard']
    if len(opponent.discard_pile) and discards_left:
        discard_num = min(discards_left, len(opponent.discard_pile))
        to_discard = sample(opponent.discard_pile, discard_num)
        opponent.discard_pile = list(filter(lambda x: x not in to_discard, opponent.discard_pile))
        state.trash_pile.extend(to_discard)
        discards_left -= discard_num
    if len(opponent.draw_pile) and discards_left:
        discard_num = min(discards_left, len(opponent.draw_pile))
        to_discard = sample(opponent.draw_pile, discard_num)
        opponent.draw_pile = list(filter(lambda x: x not in to_discard, opponent.draw_pile))
        state.trash_pile.extend(to_discard)
        discards_left -= discard_num
    if len(opponent.hand) and discards_left:
        discard_num = min(discards_left, len(opponent.hand))
        to_discard = sample(opponent.hand, discard_num)
        opponent.hand = list(filter(lambda x: x not in to_discard, opponent.hand))
        state.trash_pile.extend(to_discard)
        discards_left -= discard_num

def skip(state, card, player_num, **kwargs):
    state.players[player_num].draw(4)
    state.current_turn = player_num

def swap(state, card, player_num, **kwargs):
    player = state.players[player_num]
    opponent = state.players[(player_num + 1) % state.num_players]

    temp = player.discard_pile
    player.discard_pile = opponent.discard_pile
    opponent.discard_pile = temp

    temp = player.draw_pile
    player.draw_pile = opponent.draw_pile
    opponent.draw_pile = temp
