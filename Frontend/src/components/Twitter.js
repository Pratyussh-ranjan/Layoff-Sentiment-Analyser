import React from 'react';
import '../styles.css';

const Twitter = () => {
  const handleTwitterAnalysis = async () => {
    const response = await fetch('http://localhost:5000/analyze/twitter', { method: 'POST' });
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
        <h1>Twitter Integration</h1>
        <p>Connect your Twitter account to analyze the sentiment of your tweets and interactions on the platform.</p>
        {/* <a href="https://www.twitter.com" className="btn">Go to Twitter</a> */}
        <button onClick={handleTwitterAnalysis} className="btn">Analyze Twitter</button>
      </div>
    </div>
  );
};

export default Twitter;
