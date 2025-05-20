import { useState, useRef } from 'react';
import DiagnosisTable from './DiagnosisTable';

export default function Home() {
  const [c3dFiles, setC3dFiles] = useState([]);
  const [xlsxFiles, setXlsxFiles] = useState([]);
  const [diagnosisResult, setDiagnosisResult] = useState(null);

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

    //allows multiple file upload
    const formData = new FormData();
    for (let i = 0; i < selectedFiles.length; i++) {
      formData.append("files", selectedFiles[i]);
    }

    //calls upon upload c3d file upload if its a c3d file otherwise calls upon xlsx file
    const endpoint = fileType === 'c3d' ? "/upload/c3d" : "/upload/xlsx";
    fetch(`http://127.0.0.1:8000${endpoint}`, {
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

        if (fileType === 'xlsx') {
          const file = selectedFiles[0];
          const diagnosisFormData = new FormData();
          diagnosisFormData.append('file', file);

          fetch('http://127.0.0.1:8000/diagnose', {
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


  //allows user to upload new files and clears all inputs and arrays
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
        <img src='/umcg-logo.png' className='umcg-logo' alt="UMCG Logo" />
        <div className='header-button'>
          <h1>Gait Diagnosis System UMCG</h1>
          <div className="header-buttons">
            <button onClick={handleNewUpload}>New Upload</button>
          </div>
        </div>

        <img src='/rug-logo.png' className='umcg-logo' alt="RUG Logo" />
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
          <DiagnosisTable data={diagnosisResult} />
        </div>
      )}
    </div>
  );
}