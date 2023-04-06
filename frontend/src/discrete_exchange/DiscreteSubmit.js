import React, { useState, useEffect } from 'react';
import axios from 'axios';

function DiscreteSubmit(props) {
    // see: https://codefrontend.com/file-upload-reactjs/
    const [file, setFile] = useState();

    function submitFile() {
        if (file) {
            console.log("has file");
            axios.post('http://127.0.0.1:5000/discrete/submit', file, {
                headers: {
                  "Content-Type": "multipart/form-data",
                }
            });
        }
    }

    function changeFile(e) {
        console.log("file changed");
        setFile(e.target.files);
    }

    return (
        <div>
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
    </div>
  );
}

export default DiscreteSubmit;
