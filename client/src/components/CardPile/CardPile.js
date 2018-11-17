import React from 'react'
import PropTypes from 'prop-types'

import './CardPile.css'
import BlankCard from '../BlankCard'

const CardPile = ({ description, size }) => {
  return (
    <div className="CardPile">
      {size > 0 &&
        <BlankCard text={
          (
            description &&
            description + ': ' + size
          ) || size
        } />
      }
    </div>
  )
}

CardPile.propTypes = {
  description: PropTypes.string,
  size: PropTypes.number.isRequired,
}

export default CardPile