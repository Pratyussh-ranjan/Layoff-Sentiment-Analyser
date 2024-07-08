import React from 'react';
import '../styles.css';

const Services = () => {
  return (
    <div className="container">
      <div className="logo">
        <img src="assets/Layoff_logo.png" alt="Layoff Analyzer Logo" />
      </div>
      <div className="content">
        <a href="/linkedin" className="social-icon"><i className="fab fa-linkedin"></i><span> LinkedIn</span></a>
        <a href="/twitter" className="social-icon"><i className="fab fa-twitter"></i><span> Twitter</span></a>
      </div>
    </div>
  );
};

export default Services;
