import React from 'react'
import PropTypes from 'prop-types'

import './BlankCardRow.css'
import BlankCard from '../BlankCard'

const BlankCardRow = ({ length, text }) => {
  return (
    <div className="BlankCardRow">
      {Array(length).fill(null).map(() =>
        <BlankCard text={text} />
      )}
    </div>
  )
}

BlankCardRow.propTypes = {
  length: PropTypes.number.isRequired,
  text: PropTypes.string,
}

export default BlankCardRow
