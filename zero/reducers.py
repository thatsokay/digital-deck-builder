from . import abilities

def parse_path(root, path):
    if len(path) == 0:
        return [root]
    return [root] + parse_path(root[path[0]], path[1:])

def root_reducer(state, action, player_num):
    if not state.game_over():
        action_type = action.get('type')
        if action_type == 'end_turn':
            if player_num == state.current_turn:
                state.next_turn()
            return state
        elif action_type == 'select_card':
            return select_card_reducer(state, action, player_num)

def execute_ability(state, card, player_num, execution_type):
    for ability in card.abilities.get(execution_type, []):
        getattr(
            abilities,
            ability['ability_type']
        )(state, card, player_num, **ability.get('args', {}))

def select_card_reducer(state, action, player_num):
    if player_num != state.current_turn:
        return state
    try:
        locations = parse_path(state, action['location'])
    except (IndexError, KeyError, TypeError):
        return state

    if len(locations) == 5:
        player = state.get_current_player()
        if locations[3] is player.hand:
            # Play card from hand
            card = locations[4]
            player.hand.remove(card)
            player.in_play.append(card)
            execute_ability(state, card, player_num, 'primary')
        return state
    elif len(locations) == 3:
        if locations[1] == state.trade_row:
            player = state.get_current_player()
            card = locations[2]
            index = action['location'][1]
            # Check player resources
            for resource, amount in card.cost.items():
                if player.resources[resource] < amount:
                    return state
            # Spend player resources
            for resource, amount in card.cost.items():
                player.resources[resource] -= amount
            # Replace trade row
            try:
                replacement = state.trade_deck.pop(0)
            except IndexError:
                replacement = None
            state.trade_row = state.trade_row[:index] + (replacement,) + state.trade_row[index + 1:]
            player.discard_pile.append(card)
            return state
    else:
        return state
