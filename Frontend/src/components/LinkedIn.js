import React from 'react';
import '../styles.css';

const LinkedIn = () => {
  const handleLinkedInAnalysis = async () => {
    const response = await fetch('http://localhost:5000/analyze/linkedin', { method: 'POST' });
    const data = await response.json();
    console.log(data.message);
  };

  return (
    <div className="container">
      <div className="left-section">
        <div className="logo">
          <img src="assets/Layoff_logo.png" alt="Layoff Analyzer Logo" />
        </div>
        <div className="title">
          {/* LAYOFF ANALYZER */}
        </div>
      </div>
      <div className="content">
        <h1>LinkedIn Integration</h1>
        <p>Connect your LinkedIn account to analyze the sentiment of your posts and interactions on the platform.</p>
        {/* <a href="https://www.linkedin.com" className="btn">Go to LinkedIn</a> */}
        <button onClick={handleLinkedInAnalysis} className="btn">Analyze LinkedIn</button>
      </div>
    </div>
  );
};

export default LinkedIn;
