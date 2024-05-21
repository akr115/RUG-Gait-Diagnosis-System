import React from 'react';
import { Route, Routes } from 'react-router-dom';
import './App.css';
import umcg_logo from './umcg-logo.png';
import rug_logo from './rug-logo.png'
import Auth from './Auth';

function Home() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={umcg_logo} className='umcg-logo'/>
        <h1>Gait Diagnosis System UMCG</h1>
        <img src={rug_logo} className='umcg-logo'/>

      </header>
      <div className="data-box">
        <button>Upload Data</button>
      </div>
    </div>
  );
}

function App() {
  return (
    <Routes>
      <Route path="/auth" element={<Auth />} />
      <Route path="/" element={<Home />} />
    </Routes>
  );
}

export default App;
