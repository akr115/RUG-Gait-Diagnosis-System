import React from 'react';
import './App.css';
import umcg_logo from './umcg-logo.png';
import rug_logo from './rug-logo.png'

function App() {
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

export default App;
