import React from 'react';
import '../styles.css';

const Home = () => {
  return (
    <div className="container">
      <div className="logo">
        <img src="./assets/Layoff_logo.png" alt="Layoff Analyzer Logo" />
      </div>
      <div className="content">
        <a href="/services" className="btn">Let's Get Started</a>
      </div>
    </div>
  );
};

export default Home;
