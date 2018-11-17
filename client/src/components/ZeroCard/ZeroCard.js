import React from 'react'
import PropTypes from 'prop-types'

import './ZeroCard.css'

const ZeroCard = ({ card, handleCardClick }) => {
  return (
    <div onClick={handleCardClick([])} className={
      'ZeroCard' +
      (card.color ? ' color-' + card.color.toLowerCase().replace(/ /g, '-') : '')
    }>
      <div className="zcard-header">
        {card.cost[card.color]}
      </div>
      <div className="zcard-body">
        {card.name}
      </div>
      <div className="zcard-footer"></div>
    </div>
  )
}

ZeroCard.propTypes = {
  card: PropTypes.shape({
    name: PropTypes.string.isRequired,
    cost: PropTypes.object.isRequired,
    color: PropTypes.string.isRequired,
    abilities: PropTypes.object.isRequired,
  }),
  handleCardClick: PropTypes.func,
}

export default ZeroCard
