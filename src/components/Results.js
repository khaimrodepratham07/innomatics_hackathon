import React from 'react';
import './Results.css';

function Results({ response }) {
  if (!response) {
    return null;
  }

  const getBadgeClass = (verdict) => {
    switch (verdict) {
      case 'High':
        return 'badge-success';
      case 'Medium':
        return 'badge-warning';
      case 'Low':
        return 'badge-danger';
      default:
        return 'badge-secondary';
    }
  };

  return (
    <div className="Results">
      <h2>Results</h2>
      {response.results ? (
        response.results.map((result, index) => (
          <div key={index} className="result-card">
            <h3>{result.filename}</h3>
            <p>
              <strong>Score:</strong> {result.score}
              <span className={`badge ${getBadgeClass(result.fit_verdict)} ml-2`}>
                {result.fit_verdict}
              </span>
            </p>
            <div>
              <strong>Found Skills:</strong>
              <ul className="skills-list">
                {result.found_skills.map((skill, i) => (
                  <li key={i}>{skill}</li>
                ))}
              </ul>
            </div>
            <div>
              <strong>Missing Skills:</strong>
              <ul className="skills-list">
                {result.missing_skills.map((skill, i) => (
                  <li key={i}>{skill}</li>
                ))}
              </ul>
            </div>
            <p className="feedback">{result.feedback}</p>
          </div>
        ))
      ) : (
        <pre>{JSON.stringify(response, null, 2)}</pre>
      )}
    </div>
  );
}

export default Results;