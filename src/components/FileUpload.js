import React from 'react';
import './FileUpload.css';

function FileUpload({ onJdChange, onResumeChange, onSubmit }) {
  return (
    <form onSubmit={onSubmit} className="FileUpload">
      <div className="form-group">
        <label htmlFor="jd">Job Description (JD)</label>
        <input type="file" id="jd" accept=".txt,.pdf,.docx" onChange={onJdChange} required />
      </div>
      <div className="form-group">
        <label htmlFor="resumes">Resumes</label>
        <input type="file" id="resumes" accept=".pdf,.docx" onChange={onResumeChange} multiple required />
      </div>
      <button type="submit">Check Relevance</button>
    </form>
  );
}

export default FileUpload;
