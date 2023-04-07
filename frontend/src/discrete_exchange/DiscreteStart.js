import React, { useState, useEffect } from 'react';
import axios from 'axios';

function DiscreteStart(props) {
    function startGame() {
        axios.post('http://127.0.0.1:5000/discrete/start', {
            gameId: 'test_game',
            }, {
                headers: {
                    "Content-Type": "multipart/form-data",
                }
            }
        );
    }

    return (
        <div>
            Start the discrete exchange
            <br />
            <button onClick={startGame}>
                Start Game
            </button>
        </div>
  );
}

export default DiscreteStart;
