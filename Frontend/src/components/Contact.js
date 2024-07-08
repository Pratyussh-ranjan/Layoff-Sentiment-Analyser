import React from 'react';
import '../styles.css';

const Contact = () => {
  return (
    <div className="container">
      <div className="logo">
        <img src="assets/Layoff_logo.png" alt="Layoff Analyzer Logo" />
      </div>
      <div className="heading">
        <h1>Contact Us</h1>
      </div>
      <div className="content">
        <p>If you have any questions or need further information, please feel free to contact us at:</p>
        <p>Email: info@mysite.com<br />Phone: 123-456-7890</p>
      </div>
    </div>
  );
};

export default Contact;
