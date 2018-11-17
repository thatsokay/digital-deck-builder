import React from 'react'
import PropTypes from 'prop-types'

import './BlankCard.css'

const BlankCard = ({ text }) => {
  return (
    <div className="BlankCard">
      {text}
    </div>
  )
}

BlankCard.propTypes = {
  text: PropTypes.string,
}

export default BlankCard
