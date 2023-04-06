import React, { useState, useEffect } from 'react';

function DiscreteSubmit(props) {
  return (
    <div>
      Please submit your trader code below
      <form>
        <label>
            Select .py file 
        </label>
        <input type='file' name='trader'/>
      </form>
    </div>
  );
}

export default DiscreteSubmit;
