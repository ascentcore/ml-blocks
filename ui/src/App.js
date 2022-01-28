import React from 'react';
import {
  BrowserRouter as Router,
  Route
} from 'react-router-dom';
import './App.css';
import Layout from './components/Layout';
import HomeScreen from './screens/HomeScreen';

function App() {
  return (
    <div className="App">
      <Layout>
        <Router>
          <Route path='/' component={HomeScreen} />
        </Router>
      </Layout>
    </div>
  );
}

export default App;
