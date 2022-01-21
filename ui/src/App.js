import React from 'react';
import { Route } from 'react-router-dom';
import './App.css';
import Routes from './Routes';

function App() {
  return (
    <div className="App">
      <Route component={Routes} />
    </div>
  );
}

export default App;
