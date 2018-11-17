import React from 'react'
import PropTypes from 'prop-types'

import StarRealmsCard from '../StarRealmsCard'
import ZeroCard from '../ZeroCard'
import './CardRow.css'

const CardRow = ({ gameName, cards, handleCardClick }) => {
  return (
    <div className="CardRow">
      {
        cards.map((card, index) => (
          card && (
            (
              gameName === 'star_realms' &&
              <StarRealmsCard handleCardClick={handleCardClick(index)} card={card} />
            ) ||
            (
              gameName === 'zero' &&
              <ZeroCard handleCardClick={handleCardClick(index)} card={card} />
            )
          )
        ) ||
        <div className="empty" />
      )}
    </div>
  )
}

CardRow.propTypes = {
  game: PropTypes.string,
  cards: PropTypes.array,
  handleCardClick: PropTypes.func,
}

export default CardRow
