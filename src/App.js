import React, { useState } from 'react';
import './App.css';
import Header from './components/Header';
import FileUpload from './components/FileUpload';
import Results from './components/Results';
import { Oval } from 'react-loader-spinner';

function App() {
  const [jdFile, setJdFile] = useState(null);
  const [resumeFiles, setResumeFiles] = useState([]);
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleJdChange = (e) => {
    setJdFile(e.target.files[0]);
  };

  const handleResumeChange = (e) => {
    setResumeFiles(e.target.files);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const formData = new FormData();
    formData.append('jd', jdFile);
    for (let i = 0; i < resumeFiles.length; i++) {
      formData.append('resumes', resumeFiles[i]);
    }

    try {
      const res = await fetch('http://127.0.0.1:5000/upload', {
        method: 'POST',
        body: formData,
      });
      const data = await res.json();
      setResponse(data);
    } catch (error) {
      console.error('Error uploading files:', error);
      setResponse({ error: 'Failed to upload files. Make sure the backend is running.' });
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <Header />
      <main>
        <FileUpload
          onJdChange={handleJdChange}
          onResumeChange={handleResumeChange}
          onSubmit={handleSubmit}
        />
        {loading ? (
          <Oval
            height={80}
            width={80}
            color="#4fa94d"
            wrapperStyle={{}}
            wrapperClass=""
            visible={true}
            ariaLabel='oval-loading'
            secondaryColor="#4fa94d"
            strokeWidth={2}
            strokeWidthSecondary={2}
          />
        ) : (
          <Results response={response} />
        )}
      </main>
    </div>
  );
}

export default App;