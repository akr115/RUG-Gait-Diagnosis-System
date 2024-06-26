import React from 'react';

function DiagnosisTable({ data }) {
  // Ensure data is parsed from JSON if it's a string
  const [diagnosisJson, loJson] = data.map(item => JSON.parse(item));

  // Extract necessary data for the diagnosis table
  const diagnoses = Object.values(diagnosisJson.Diagnosis || {});
  const jointFoot = Object.values(diagnosisJson['Joint Foot'] || {});
  const events = Object.values(diagnosisJson.Event || {});
  const joints = Object.values(diagnosisJson.Joint || {});
  const eventFoots = Object.values(diagnosisJson['Event Foot'] || {});

  // Extract necessary data for the LO table
  const loNames = Object.values(loJson.Name || {});
  const loValues = Object.values(loJson.Value || {});

  // Render the LO table
  const renderLOTable = () => (
    <div className="lo-table">
      <h2>LO Table</h2>
      <table>
        <thead>
          <tr>
            <th>Name</th>
            <th>Value</th>
          </tr>
        </thead>
        <tbody>
          {loNames.map((name, index) => (
            <tr key={index}>
              <td>{name}</td>
              <td>{loValues[index]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );

  // Render the general diagnosis table
  const renderGeneralTable = () => (
    <div className="general-table">
      <h2>General Diagnosis Table</h2>
      <table>
        <thead>
          <tr>
            <th>Diagnosis</th>
            <th>Joint Foot</th>
            <th>Joint</th>
            <th>Event Foot</th>
            <th>Event</th>
          </tr>
        </thead>
        <tbody>
          {diagnoses.map((diag, index) => (
            <tr key={index}>
              <td>{diag}</td>
              <td>{jointFoot[index]}</td>
              <td>{joints[index]}</td>
              <td>{eventFoots[index]}</td>
              <td>{events[index]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );

  return (
    <div className="App">
      {renderLOTable()}
      {renderGeneralTable()}
    </div>
  );
}

export default DiagnosisTable;
