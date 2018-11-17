import React from 'react'
import { Route, Switch } from 'react-router-dom'

import './App.css'
import Home from '../Home'
import Board from '../Board'

const App = () => (
  <div className="App">
    <Switch>
      <Route exact path="/" component={Home} />
      <Route path="/game/:gameName" component={Board} />
    </Switch>
  </div>
)

export default App
