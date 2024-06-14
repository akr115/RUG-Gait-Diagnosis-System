import React, { useState } from 'react';
import { Route, Routes } from 'react-router-dom';
import './App.css';
import umcg_logo from './umcg-logo.png';
import rug_logo from './rug-logo.png';
import Auth from './Auth';

function Home() {
  const [selectedFiles, setSelectedFiles] = useState([]);

  const handleFileChange = (event) => {
    setSelectedFiles(event.target.files);
  };

  const handleUpload = () => {
    if (selectedFiles.length === 0) {
      alert("Please select files first!");
      return;
    }
    const formData = new FormData();
    for (let i = 0; i < selectedFiles.length; i++) {
      formData.append("files", selectedFiles[i]);
    }

    fetch("http://localhost:5000/upload", {
      method: "POST",
      body: formData,
      credentials: 'include'  // Ensure cookies are included if needed
    })
      .then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        console.log("Files uploaded successfully:", data);
        alert("Files uploaded successfully!");
      })
      .catch(error => {
        console.error("Error uploading files:", error);
        alert("Error uploading files. Please try again.");
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
        <input type="file" accept=".c3d,.xlsx" multiple onChange={handleFileChange} />
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
