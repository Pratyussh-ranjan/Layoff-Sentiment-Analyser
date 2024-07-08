import React from 'react';
import { Link } from 'react-router-dom';
import '../styles.css';

const Header = () => {
  return (
    <header>
      <div className="navigation">
        <Link to="/">HOME</Link>
        <Link to="/about">ABOUT US</Link>
        <Link to="/services">OUR SERVICES</Link>
        <Link to="/contact">CONTACT</Link>
      </div>
    </header>
  );
};

export default Header;
