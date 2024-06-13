import React, { useState } from 'react';
import { Route, Routes } from 'react-router-dom';
import './App.css';
import umcg_logo from './umcg-logo.png';
import rug_logo from './rug-logo.png';
import Auth from './Auth';

function Home() {
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = () => {
    if (!selectedFile) {
      alert("Please select a file first!");
      return;
    }
    const formData = new FormData();
    formData.append("file", selectedFile);

    fetch("/upload", {
      method: "POST",
      body: formData,
    })
      .then(response => response.json())
      .then(data => {
        console.log("File uploaded successfully:", data);
      })
      .catch(error => {
        console.error("Error uploading file:", error);
      });
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={umcg_logo} className='umcg-logo' alt="UMCG Logo" />
        <h1>Gait Diagnosis System UMCG</h1>
        <img src={rug_logo} className='umcg-logo' alt="RUG Logo" />
      </header>
      <div className="data-box">
        <input type="file" accept=".c3d,.xlsx" onChange={handleFileChange} />
        <button onClick={handleUpload}>Upload Data</button>
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
