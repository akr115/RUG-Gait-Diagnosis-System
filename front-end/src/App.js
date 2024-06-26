import React, { useState, useRef } from 'react';
import { Routes, Route, useNavigate, Navigate } from 'react-router-dom';
import { useAuth } from './AuthContext';
import './App.css';
import umcg_logo from './umcg-logo.png';
import rug_logo from './rug-logo.png';
import DiagnosisTable from './DiagnosisTable';
import Auth from './Auth';
import ProtectedRoute from './ProtectedRoute';

function Home() {
  const [c3dFiles, setC3dFiles] = useState([]);
  const [xlsxFiles, setXlsxFiles] = useState([]);
  const [diagnosisResult, setDiagnosisResult] = useState(null); // State to store diagnosis result
  const { logout } = useAuth();
  const navigate = useNavigate();

  const c3dInputRef = useRef(null);
  const xlsxInputRef = useRef(null);

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
    fetch(`http://127.0.0.1:5000${endpoint}`, {
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

        // Call the diagnosis endpoint if the files are XLSX
        if (fileType === 'xlsx') {
          const file = selectedFiles[0]; // Assuming only one XLSX file is uploaded for diagnosis
          const diagnosisFormData = new FormData();
          diagnosisFormData.append('file', file);

          fetch('http://127.0.0.1:5000/diagnose', {
            method: 'POST',
            body: diagnosisFormData,
            credentials: 'include'
          })
            .then(response => {
              if (!response.ok) {
                throw new Error('Network response was not ok');
              }
              return response.json();
            })
            .then(diagnosisData => {
              console.log("Diagnosis result:", diagnosisData);
              setDiagnosisResult(diagnosisData); // Set the diagnosis result
            })
            .catch(error => {
              console.error("Error during diagnosis:", error);
              alert("Error during diagnosis. Please try again.");
            });
        }
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

  const handleNewUpload = () => {
    setC3dFiles([]);
    setXlsxFiles([]);
    setDiagnosisResult(null);
    if (c3dInputRef.current) c3dInputRef.current.value = '';
    if (xlsxInputRef.current) xlsxInputRef.current.value = '';
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={umcg_logo} className='umcg-logo' alt="UMCG Logo" />
        <div className='header-button'>
          <h1>Gait Diagnosis System UMCG</h1>
          <div className="header-buttons">
            <button onClick={handleLogout}>Logout</button>
            <button onClick={handleNewUpload}>New Upload</button>
          </div>
        </div>

        <img src={rug_logo} className='umcg-logo' alt="RUG Logo" />
      </header>

      <div className="data-box">
        <div>
          <input type="file" accept=".c3d" multiple onChange={handleC3dFileChange} ref={c3dInputRef} />
          <button onClick={() => handleUpload('c3d')}>Upload C3D Files</button>
        </div>
        <div>
          <input type="file" accept=".xlsx" multiple onChange={handleXlsxFileChange} ref={xlsxInputRef} />
          <button onClick={() => handleUpload('xlsx')}>Upload XLSX Files</button>
        </div>
      </div>
      {diagnosisResult && (
        <div className="diagnosis-result">
          <h2>Diagnosis Result</h2>
          <DiagnosisTable data={diagnosisResult} />
        </div>
      )}
    </div>
  );
}

function App() {
  return (
    <Routes>
      <Route path="/auth" element={<Auth />} />
      <Route path="/upload" element={<ProtectedRoute element={<Home />} />} />
      <Route path="" element={<Navigate to="/auth" />} />
    </Routes>
  );
}

export default App;
