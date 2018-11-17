from .reducers import parse_path
from .card import Base

def resource(state, card, player_num, **kwargs):
    player = state.players[player_num]
    for resource_type, amount in kwargs.items():
        player.add_resource(resource_type, amount)

def objective(state, card, player_num, **kwargs):
    player = state.players[player_num]
    for objective_type, amount in kwargs.items():
        player.add_objective(objective_type, amount)

def draw(state, card, player_num, **kwargs):
    player = state.players[player_num]
    player.draw(kwargs['draw'])

def scrap_trade(state, card, player_num, **kwargs):
    def choice_reducer(inner_state, action, inner_player_num):
        if inner_player_num != player_num:
            inner_state.pending_choices.append(choice_reducer)
            return inner_state
        else:
            try:
                locations = parse_path(inner_state, action['location'])
            except (IndexError, KeyError, TypeError):
                inner_state.pending_choices.append(choice_reducer)
                return inner_state
            if len(locations) < 4:
                inner_state.pending_choices.append(choice_reducer)
                return inner_state
            elif locations[1] is inner_state.trade_row:
                try:
                    card = inner_state.buy_card(action['location'][1])
                except IndexError:
                    inner_state.pending_choices.append(choice_reducer)
                    return inner_state
                inner_state.trash_pile.append(card)
                return inner_state
            else:
                inner_state.pending_choices.append(choice_reducer)
                return inner_state

    if state.trade_row != (None, None, None, None, None):
        state.pending_choices.append(choice_reducer)

def scrap_hand_discard(state, card, player_num, **kwargs):
    def choice_reducer(inner_state, action, inner_player_num):
        if inner_player_num != player_num:
            inner_state.pending_choices.append(choice_reducer)
            return inner_state
        else:
            player = inner_state.players[player_num]
            try:
                locations = parse_path(inner_state, action['location'])
            except (IndexError, KeyError, TypeError):
                inner_state.pending_choices.append(choice_reducer)
                return inner_state
            if len(locations) < 6:
                inner_state.pending_choices.append(choice_reducer)
                return inner_state
            elif locations[3] is player.hand:
                card = locations[4]
                player.hand.remove(card)
                inner_state.trash_pile.append(card)
                return inner_state
            else:
                inner_state.pending_choices.append(choice_reducer)
                return inner_state

    if len(state.players[player_num].hand) != 0:
        state.pending_choices.append(choice_reducer)

def opponent_discard(state, card, player_num, **kwargs):
    def choice_reducer(inner_state, action, inner_player_num):
        if inner_player_num != (player_num + 1) % inner_state.num_players:
            inner_state.pending_choices.append(choice_reducer)
            return inner_state
        else:
            opponent = inner_state.players[inner_player_num]
            try:
                locations = parse_path(inner_state, action['location'])
            except (IndexError, KeyError, TypeError):
                inner_state.pending_choices.append(choice_reducer)
                return inner_state
            if len(locations) < 6:
                inner_state.pending_choices.append(choice_reducer)
                return inner_state
            elif locations[3] is opponent.hand:
                card = locations[4]
                opponent.hand.remove(card)
                opponent.discard_pile.append(card)
                return inner_state
            else:
                inner_state.pending_choices.append(choice_reducer)
                return inner_state

    if len(state.players[(player_num + 1) % state.num_players].hand) != 0:
        state.pending_choices.append(choice_reducer)

def embassy_yacht(state, card, player_num, **kwargs):
    player = state.players[player_num]
    if len([played for played in player.in_play if type(played) is Base]) >= 2:
        player.draw(2)
    return state
