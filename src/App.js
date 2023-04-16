import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [transcription, setTranscription] = useState(null);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();

    if (!file) {
      alert('Please select a file to upload.');
      return;
    }

    setLoading(true);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await axios.post('/api/transcribe', formData);
      setTranscription(response.data.transcription);
    } catch (error) {
      alert('Error occurred while transcribing the audio file.');
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = () => {
    const element = document.createElement('a');
    const file = new Blob([transcription], { type: 'text/plain' });
    element.href = URL.createObjectURL(file);
    element.download = 'output.txt';
    document.body.appendChild(element);
    element.click();
  };

  const handleReset = () => {
    setFile(null);
    setTranscription(null);
  };

  return (
    <div className="App">
      <h1>EzNotes</h1>
      {!transcription ? (
        <form onSubmit={handleSubmit}>
          <input type="file" accept=".mp3" onChange={handleFileChange} />
          <button type="submit" disabled={loading}>
            {loading ? 'Transcribing...' : 'Upload'}
          </button>
        </form>
      ) : (
        <div>
          <h2>Download Preview</h2>
          <pre>{transcription}</pre>
          <button onClick={handleDownload}>Download</button>
          <button onClick={handleReset}>Restart</button>
        </div>
      )}
    </div>
  );
}

export default App;
