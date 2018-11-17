import React from 'react'
import { Link } from 'react-router-dom'

import './Home.css'

class Home extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      location: 'game/star_realms',
    }

    this.handleChange = this.handleChange.bind(this)
    this.handleJoinClick = this.handleJoinClick.bind(this)
  }

  handleChange(event) {
    this.setState({location: event.target.value})
  }

  handleJoinClick(event) {
    this.props.history.push(this.state.location)
  }

  render() {
    return (
      <div className="Home">
        <section className="hero is-fullheight">
          <div className="hero-body">
            <div className="container has-text-centered">
              <h1 className="title">Digital Deck Builder</h1>
              <select value={this.state.location} onChange={this.handleChange}>
                <option value="game/star_realms">Star Realms</option>
                <option value="game/zero">Zero</option>
              </select>
              <button onClick={this.handleJoinClick}>Join Game</button>
            </div>
          </div>
        </section>
      </div>
    )
  }
}

export default Home
