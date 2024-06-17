import React, { useState } from 'react';
import { Route, Routes, Navigate, useNavigate } from 'react-router-dom';
import { useAuth } from './AuthContext';
import './App.css';
import umcg_logo from './umcg-logo.png';
import rug_logo from './rug-logo.png';
import Auth from './Auth';
import ProtectedRoute from './ProtectedRoute';

function Home() {
  const [c3dFiles, setC3dFiles] = useState([]);
  const [xlsxFiles, setXlsxFiles] = useState([]);
  const { logout } = useAuth();
  const navigate = useNavigate();


  const handleC3dFileChange = (event) => {
    setC3dFiles(event.target.files);
  };

  const handleXlsxFileChange = (event) => {
    setXlsxFiles(event.target.files);
  };

  const handleUpload = (fileType) => {
    const selectedFiles = fileType === 'c3d' ? c3dFiles : xlsxFiles;
    if (selectedFiles.length === 0) {
      alert("Please select files first!");
      return;
    }
    const formData = new FormData();
    for (let i = 0; i < selectedFiles.length; i++) {
      formData.append("files", selectedFiles[i]);
    }

    const endpoint = fileType === 'c3d' ? "/upload/c3d" : "/upload/xlsx";
    fetch(`http://localhost:5000${endpoint}`, {
      method: "POST",
      body: formData,
      credentials: 'include'
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

  const handleLogout = () => {
    logout();
    navigate('/auth');
  };
  

  return (
    <div className="App">
      <header className="App-header">
        <img src={umcg_logo} className='umcg-logo' alt="UMCG Logo" />
        <h1>Gait Diagnosis System UMCG</h1>
        <img src={rug_logo} className='umcg-logo' alt="RUG Logo" />
        <button onClick={handleLogout}>Logout</button>
      </header>
      <div className="data-box">
        <div>
          <input type="file" accept=".c3d" multiple onChange={handleC3dFileChange} />
          <button onClick={() => handleUpload('c3d')}>Upload C3D Files</button>
        </div>
        <div>
          <input type="file" accept=".xlsx" multiple onChange={handleXlsxFileChange} />
          <button onClick={() => handleUpload('xlsx')}>Upload XLSX Files</button>
        </div>
      </div>
    </div>
  );
}

function App() {
  return (
    <Routes>
      <Route path="/auth" element={<Auth />} />
      {/* <Route path="/upload" element={<Home />} /> */}
      <Route path="/upload" element={<ProtectedRoute element={<Home />} />} />
      <Route path="" element={<Navigate to="/auth" />} />
    </Routes>
  );
}

export default App;
