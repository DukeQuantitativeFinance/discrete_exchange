import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function DiscreteResults(props) {
    const [id, setId] = useState(null);
    const [pnl, setPnl] = useState(0);

    const nav = useNavigate();

    useEffect(() => {
        setId(props.id);
    }, [props.id])

    axios.post('http://127.0.0.1:5000/discrete/results', {
            userId: props.id,
            gameId: 'test_game',
        }, {
            headers: {
                "Content-Type": "multipart/form-data",
            }
        }
    ).then((response) => {
        console.log("response: ", response);
        setPnl(response.data.pnl);
    }).catch((response) => {
        console.log("pnl not found");
    });

    function viewSubmit() {
        nav('/discrete/submit');
    }

    return (
        <div>
            View the results of the game
            <br />
            Your id: {props.id}
            <br />
            Your pnl: {pnl}
            <br />
            <button onClick={viewSubmit}>
                Back
            </button>
        </div>
    );
}

export default DiscreteResults;
