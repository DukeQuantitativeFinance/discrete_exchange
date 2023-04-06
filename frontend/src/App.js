import React, { useState, useEffect } from 'react';
import { Routes, Route, BrowserRouter } from 'react-router-dom';

import './App.css';
import DiscreteHome from './discrete_exchange/DiscreteHome';
import DiscreteSubmit from './discrete_exchange/DiscreteSubmit';
import DiscreteResults from './discrete_exchange/DiscreteResults';

function App() {
  return (
    <div className='App'>
      <Routes>
        {/* DISCRETE EXCHANGE HOME PAGE */}
        <Route
          exact
          path={'/discrete'}
          element={<DiscreteHome />}
        />

        {/* DISCRETE EXCHANGE SUBMIT PAGE */}
        <Route
          exact
          path={'/discrete/submit'}
          element={<DiscreteSubmit />}
        />

        {/* DISCRETE EXCHANGE RESULTS PAGE */}
        <Route
          exact
          path={'/discrete/results'}
          element={<DiscreteResults />}
        />
      </Routes>
    </div>
  );
}

export default App;
