import React from 'react'
import socketio from 'socket.io-client'

import './Board.css'
import CardRow from '../../components/CardRow'
import BlankCardRow from '../../components/BlankCardRow'
import CardPile from '../../components/CardPile'

class Board extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      socket: socketio(),
      gameName: this.props.match.params.gameName,
      playerNum: null,
      gameState: {},
    }

    this.componentDidMount = this.componentDidMount.bind(this)
    this.onJoin = this.onJoin.bind(this)
    this.onStart = this.onStart.bind(this)
    this.onUpdate = this.onUpdate.bind(this)
    this.handleEndTurn = this.handleEndTurn.bind(this)
    this.descendParse = this.descendParse.bind(this)
  }

  componentDidMount() {
    this.state.socket.emit('join', {'game_name': this.state.gameName})
    this.state.socket.on('join', this.onJoin)
    this.state.socket.on('start', this.onStart)
    this.state.socket.on('update', this.onUpdate)
  }

  onJoin(msg) {
    this.setState({gameName: msg.game_name, playerNum: msg.player_num})
  }

  onStart(msg) {
    this.setState({gameState: msg})
  }

  onUpdate(msg) {
    this.setState({gameState: msg})
    let gameOver = false
    let lose = false
    switch (this.state.gameName) {
      case 'star_realms':
        for (let i = 0; i < this.state.gameState.players.length; i++) {
          if (this.state.gameState.players[i].objectives.authority <= 0) {
            if (i === this.state.playerNum) {
              lose = true
            }
            gameOver = true
          }
        }
        if (gameOver) {
          if (lose) {
            alert('You lose')
          } else {
            alert('You win')
          }
        }
        break
      case 'zero':
        for (let i = 0; i < this.state.gameState.players.length; i++) {
          const player = this.state.gameState.players[i]
          if (player.hand.length + player.draw_pile.length + player.discard_pile.length + player.in_play.length === 0) {
            if (i === this.state.playerNum) {
              lose = true
            }
            gameOver = true
          }
        }
        if (gameOver) {
          if (lose) {
            alert('You lose')
          } else {
            alert('You win')
          }
        }
        break
      default:
    }
  }

  handleEndTurn() {
    this.state.socket.emit('action', {
      type: 'end_turn',
    })
  }

  handleCardClick = domain => index => section => () => {
    this.state.socket.emit('action', {
      type: 'select_card',
      location: [...domain, index, ...section],
    })
  }

  handlePlayerClick = playerNum => () => {
    this.state.socket.emit('action', {
      type: 'select_player',
      selected_player: playerNum,
    })
  }

  descendParse(initial, attributes, fallback) {
    if (initial === undefined) {
      return fallback
    } else if (!attributes.length) {
      return initial
    } else {
      return this.descendParse(
        initial[attributes[0]],
        attributes.slice(1),
        fallback,
      )
    }
  }

  render() {
    return (
      <div className="Board">
        <div className="opponent-discard">
          <CardPile description={'Opponent Discard Pile'}
            size={
              this.descendParse(
                this.state.gameState,
                ['players', (this.state.playerNum + 1) % 2, 'discard_pile'],
                [],
              ).length
            }
          />
        </div>
        <div className="opponent-hand">
          <BlankCardRow length={
            this.descendParse(
              this.state.gameState,
              ['players', (this.state.playerNum + 1) % 2, 'hand'],
              [],
            ).length
          } />
        </div>
        <div className="opponent-draw">
          <CardPile description={'Opponent Draw Pile'}
            size={
              this.descendParse(
                this.state.gameState,
                ['players', (this.state.playerNum + 1) % 2, 'draw_pile'],
                [],
              ).length
            }
          />
        </div>
        <div className="opponent-play">
          <CardRow
            gameName={this.state.gameName}
            handleCardClick={
              this.handleCardClick(
                ['players', (this.state.playerNum + 1) % 2, 'in_play']
              )
            }
            cards={
              this.descendParse(
                this.state.gameState,
                ['players', (this.state.playerNum + 1) % 2, 'in_play'],
                [],
              )
            }
          />
        </div>
        <div onClick={this.handlePlayerClick((this.state.playerNum + 1) % 2)} className="opponent-stats">
          {Object.entries(this.descendParse(
            this.state.gameState,
            ['players', (this.state.playerNum + 1) % 2, 'objectives'],
            {},
          )).concat(Object.entries(this.descendParse(
            this.state.gameState,
            ['players', (this.state.playerNum + 1) % 2, 'resources'],
            {},
          ))).map((pair) =>
            <p className="stat">{pair[0]}: {pair[1]}</p>
          )}
        </div>
        <div className="trash-pile">
          <CardPile description={'Trash Pile'}
            size={
              this.descendParse(this.state.gameState, ['trash_pile'], []).length
            }
          />
        </div>
        <div className="trade-row">
          <CardRow
            gameName={this.state.gameName}
            handleCardClick={this.handleCardClick(['trade_row'])}
            cards={this.descendParse(this.state.gameState, ['trade_row'], [])}
          />
        </div>
        <div className="trade-deck">
          <CardPile description={'Trade Deck'}
            size={
              this.descendParse(this.state.gameState, ['trade_deck'], []).length
            }
          />
        </div>
        <div className="own-play">
          <CardRow
            gameName={this.state.gameName}
            handleCardClick={
              this.handleCardClick(
                ['players', this.state.playerNum, 'in_play']
              )
            }
            cards={
              this.descendParse(
                this.state.gameState,
                ['players', this.state.playerNum, 'in_play'],
                [],
              )
            }
          />
        </div>
        <div onClick={this.handlePlayerClick(this.state.playerNum)} className="own-stats">
          <p><strong>{
            this.state.playerNum === this.descendParse(
              this.state.gameState,
              ['current_turn'],
              null,
            ) ? 'Your Turn' : "Opponent's Turn"
          }</strong></p>
          {Object.entries(this.descendParse(
            this.state.gameState,
            ['players', this.state.playerNum, 'objectives'],
            {},
          )).concat(Object.entries(this.descendParse(
            this.state.gameState,
            ['players', this.state.playerNum, 'resources'],
            {},
          ))).map((pair) =>
            <p className="stat">{pair[0]}: {pair[1]}</p>
          )}
          <button onClick={this.handleEndTurn} className="button is-danger is-rounded">End Turn</button>
        </div>
        <div className="own-discard">
          <CardPile description={'Discard Pile'}
            size={
              this.descendParse(
                this.state.gameState,
                ['players', this.state.playerNum, 'discard_pile'],
                [],
              ).length
            }
          />
        </div>
        <div className="own-hand">
          <CardRow
            gameName={this.state.gameName}
            handleCardClick={
              this.handleCardClick(
                ['players', this.state.playerNum, 'hand']
              )
            }
            cards={
              this.descendParse(
                this.state.gameState,
                ['players', this.state.playerNum, 'hand'],
                [],
              )
            }
          />
        </div>
        <div className="own-draw">
          <CardPile description={'Draw Pile'}
            size={
              this.descendParse(
                this.state.gameState,
                ['players', this.state.playerNum, 'draw_pile'],
                [],
              ).length
            }
          />
        </div>
      </div>
    )
  }
}

export default Board
