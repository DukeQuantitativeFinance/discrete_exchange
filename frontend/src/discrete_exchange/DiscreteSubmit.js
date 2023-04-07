import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function DiscreteSubmit(props) {
    // see: https://codefrontend.com/file-upload-reactjs/
    const [name, setName] = useState('');
    const [file, setFile] = useState(null);

    const nav = useNavigate();

    useEffect(() => {
        setName(props.id);
    }, [props.id])

    function submitFile() {
        if (file) {
            console.log("has file");
            axios.post('http://127.0.0.1:5000/discrete/submit', {
                    userId: name,
                    gameId: 'test_game',
                    file,
                }, {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    }
                }
            );
            setFile(null);
            // setName('');
            // document.getElementsByName('username')[0].reset();
            // document.getElementsByName('trader')[0].reset();
        }
    }

    function changeName(e) {
        console.log(e.target.value);
        setName(e.target.value);
        props.setId(e.target.value);
    }

    function changeFile(e) {
        console.log("file changed");
        setFile(e.target.files);
    }

    function viewResults() {
        nav('/discrete/results')
    }

    return (
        <div>
            Please enter your username
            <form>
                <label>
                    <input type='text' value={name} name='username' onChange={(e) => changeName(e)}/>
                </label>
                <br />
            </form>
            Please submit your trader code below
            <br />
            <form>
                <label>
                    <input type='file' name='trader' accept='.py' onChange={(e) => changeFile(e)}/>
                </label>
                <br />
            </form>
            <button onClick={submitFile}>
                Submit
            </button>
            <br />
            <button onClick={viewResults}>
                View Results
            </button>
        </div>
  );
}

export default DiscreteSubmit;
