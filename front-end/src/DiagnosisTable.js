import React from 'react';

function DiagnosisTable({ data }) {
  // Ensure data is parsed from JSON if it's a string
  const diagnosis = typeof data === 'string' ? JSON.parse(data) : data;

  // Extract necessary data
  const diagnoses = Object.values(diagnosis.Diagnosis || {});
  const loData = Object.values(diagnosis.LO || {});
  const jointFoot = Object.values(diagnosis['Joint Foot'] || {});
  const events = Object.values(diagnosis.Event || {});
  const joints = Object.values(diagnosis.Joint || {});
  const eventFoots = Object.values(diagnosis['Event Foot'] || {});

  // Collect all unique headers from LO arrays across all diagnoses
  let allHeaders = new Set();
  loData.forEach((lo, index) => {
    if (lo.length > 0) {
      lo.forEach(item => allHeaders.add(item[0]));
    }
  });
  allHeaders = Array.from(allHeaders); // Convert Set to Array

  // Render the table
  return (
    <div className="App">
      <h2>Diagnosis Table</h2>
      <table>
        <thead>
          <tr>
            <th>Diagnosis</th>
            <th>LO</th>
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
              <td className="lo-cell">
                {loData[index]?.length > 0 ? (
                  <ul className="lo-list">
                    {loData[index].map((item, idx) => (
                      <li key={idx}>
                        <strong>{item[0]}:</strong> {item[1]}
                      </li>
                    ))}
                  </ul>
                ) : (
                  <span className="empty-lo">Empty</span>
                )}
              </td>
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
}

export default DiagnosisTable;
