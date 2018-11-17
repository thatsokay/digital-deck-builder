from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit, join_room

from star_realms.board import Board as StarRealmsBoard
from star_realms.reducers import root_reducer as starrealms_reducer
from zero.board import Board as ZeroBoard
from zero.reducers import root_reducer as zero_reducer

app = Flask(__name__, template_folder='static')
socketio = SocketIO(app)

NUM_PLAYERS = 2

player_ids = []
game_name = None
board = None
reducer = None

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('join')
def join_game(message):
    if len(player_ids) < NUM_PLAYERS:
        global game_name
        global board
        global reducer
        game_request = message.get('game_name')
        game_name = game_name or game_request
        if game_request and game_request == game_name:
            if not board:
                if game_name == 'star_realms':
                    board = StarRealmsBoard(
                        NUM_PLAYERS,
                        'star_realms/decks/start_deck.json',
                        'star_realms/decks/trade_deck.json',
                        'star_realms/decks/explorer.json',
                    )
                    reducer = starrealms_reducer
                elif game_name == 'zero':
                    board = ZeroBoard(
                        NUM_PLAYERS,
                        'zero/decks/start_deck.json',
                        'zero/decks/trade_deck.json',
                    )
                    reducer = zero_reducer
            if board:
                player_ids.append(request.sid)
                emit('join', {
                    'status': 'ACCEPTED',
                    'game_name': game_name,
                    'player_num': player_ids.index(request.sid),
                })
                join_room('current_game')
                if len(player_ids) == NUM_PLAYERS:
                    emit('start', board.dump(), room='current_game')
        else:
            emit('join', {'status': 'REJECTED', 'reason': 'Invalid game'})
    else:
        emit('join', {'status': 'REJECTED', 'reason': 'Room full'})

@socketio.on('action')
def handle_action(action):
    try:
        player_num = player_ids.index(request.sid)
        reducer(board, action, player_num)
        emit('update', board.dump(), room='current_game')
    except ValueError:
        pass

@socketio.on('disconnect')
def handle_disconnect():
    global game_name
    global board
    global reducer
    global player_ids
    emit('end', room='current_game')
    game_name = board = reducer = None
    player_ids = []

if __name__ == '__main__':
    socketio.run(app)
