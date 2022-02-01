import React from 'react';
import {
  BrowserRouter as Router,
  Route
} from 'react-router-dom';
import './App.css';
import Layout from './components/Layout';
import Routes from './Routes';
import HomeScreen from './screens/HomeScreen';

function App() {
  return (
    <div className="App">
      <Layout>
        <Router>
          <Route component={Routes} />
        </Router>
      </Layout>
    </div>
  );
}

export default App;
