from . import abilities
from .card import Base

def descend_parse(initial, path, fallback=None):
    if len(path) == 0:
        return initial
    try:
        return descend_parse(
            initial[path[0]],
            path[1:],
            fallback,
        )
    except (IndexError, KeyError, TypeError):
        return fallback

def parse_path(root, path):
    if len(path) == 0:
        return [root]
    return [root] + parse_path(root[path[0]], path[1:])

def execute_ability(state, card, player_num, execution_type):
    for ability in card.abilities.get(execution_type, []):
        getattr(
            abilities,
            ability['ability_type']
        )(state, card, player_num, **ability.get('args', {}))

def root_reducer(state, action, player_num):
    """
    Processes client actions to affect the game state.
    """
    if not state.game_over():
        if len(state.pending_choices) == 0:
            action_type = action.get('type')
            if action_type == 'end_turn':
                if player_num == state.current_turn:
                    state.next_turn()
                    for card in state.get_current_player().in_play:
                        execute_ability(state, card, state.current_turn, 'primary')
                    return state
            elif action_type == 'select_card':
                return select_card(state, action, player_num)
            elif action_type == 'select_player':
                if player_num == state.current_turn:
                    try:
                        selected = state.players[action['selected_player']]
                    except (IndexError, KeyError):
                        return state
                    if selected == state.get_current_player():
                        return state
                    if True not in [base.outpost for base in selected.in_play if type(base) is Base]:
                        combat = state.get_current_player().resources['combat']
                        state.get_current_player().resources['combat'] = 0
                        selected.objectives['authority'] -= combat
                return state
        else:
            choice_reducer = state.pending_choices.pop()
            return choice_reducer(state, action, player_num)

def select_card(state, action, player_num):
    player = state.players[player_num]
    if player is not state.get_current_player():
        return state
    try:
        locations = parse_path(state, action['location'])
    except (IndexError, KeyError, TypeError):
        return state
    if len(locations) < 4:
        return state
    if locations[3] is state.get_current_player().hand:
        # Play card from hand
        try:
            card = player.play_card(action['location'][3])
        except IndexError:
            return state
        # Execute primary abilities
        execute_ability(state, card, player_num, 'primary')
        return state
    elif locations[1] is state.trade_row:
        # Buy card from trade row
        cost = locations[2].cost
        # Check if player has sufficient resources
        for resource, amount in cost.items():
            if player.resources[resource] < amount:
                return state
        # Spend player resources
        for resource, amount in cost.items():
            player.resources[resource] -= amount
        card = state.buy_card(action['location'][1])
        player.discard_pile.append(card)
        return state
    elif locations[3] is state.get_current_player().in_play:
        try:
            card = locations[4]
            clicked = action['location'][5]
        except IndexError:
            return state
        if clicked == 'ally' and card not in player.used_ally_ability:
            faction = card.faction
            if faction in [played.faction for played in locations[3] if played is not card]:
                execute_ability(state, card, player_num, 'ally')
                player.used_ally_ability.append(card)
        elif clicked == 'scrap':
            execute_ability(state, card, player_num, 'scrap')
            player.in_play.remove(card)
            state.trash_pile.append(card)
    elif locations[3] in [opponent.in_play for opponent in state.players if opponent is not player]:
        # Attack opponent base
        opponent = locations[2]
        try:
            card = locations[4]
        except IndexError:
            return state
        if type(card) is Base and player.resources['combat'] >= card.defense:
            if card.outpost or True not in [base.outpost for base in locations[3] if type(base) is Base]:
                opponent.in_play = list(filter(lambda x: x is not card, opponent.in_play))
                opponent.discard_pile.append(card)
                player.resources['combat'] -= card.defense
        return state
