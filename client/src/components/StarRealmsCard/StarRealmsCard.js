import React from 'react'
import PropTypes from 'prop-types'

import './StarRealmsCard.css'

const StarRealmsCard = ({ card, handleCardClick }) => {
  return (
    <div className="StarRealmsCard">
      <header onClick={handleCardClick(['name'])} className={
        'srcard-header' +
        (card.faction ? ' faction-' + card.faction.toLowerCase().replace(/ /g, '-') : '')
      }>
        <div className="srcard-header-section">
          {card.card_type === 'Base' && (
            (card.outpost && <strong>{card.defense}</strong>) ||
            card.defense
          )}
        </div>
        <div className="srcard-header-section">
          {card.name}
        </div>
        <div className="srcard-header-section">
          {card.cost.trade}
        </div>
      </header>
      <div className="srcard-body">
        {card.abilities.primary &&
          <div onClick={handleCardClick(['abilities', 'primary'])} className="srcard-body-section">
            {
              card.abilities.primary.map(
                ability => ability.description
              ).join(' ')
            }
          </div>
        }
        {card.abilities.ally &&
          <div onClick={handleCardClick(['abilities', 'ally'])} className="srcard-body-section">
            <strong>Ally: </strong>
            {
              card.abilities.ally.map(
                ability => ability.description
              ).join(' ')
            }
          </div>
        }
        {card.abilities.scrap &&
          <div onClick={handleCardClick(['abilities', 'scrap'])} className="srcard-body-section">
            <strong>Scrap: </strong>
            {
              card.abilities.scrap.map(
                ability => ability.description
              ).join(' ')
            }
          </div>
        }
      </div>
    </div>
  )
}

StarRealmsCard.propTypes = {
  card: PropTypes.shape({
    name: PropTypes.string.isRequired,
    card_type: PropTypes.string.isRequired,
    cost: PropTypes.object.isRequired,
    faction: PropTypes.string,
    abilities: PropTypes.object.isRequired,
    defense: PropTypes.number,
  }),
  handleCardClick: PropTypes.func,
}

export default StarRealmsCard
