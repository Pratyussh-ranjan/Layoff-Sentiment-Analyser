import React from 'react';
import '../styles.css';

const About = () => {
  return (
    <div className="container">
      <div className="logo">
        <img src="assets/Layoff_logo.png" alt="Layoff Analyzer Logo" />
      </div>
      <div className="heading">
        <h1>About Us</h1>
      </div>
      <div className="content">
        <p>Layoff Analyzer Site is a basic analysis site where users analyze their posts for sentiments like Positive, Negative, or Neutral.</p>
        <p>Laid off workers or displaced workers are workers who have lost or left their jobs because their employer has closed or moved, there was insufficient work for them to do, or their position or shift was abolished (Borbely, 2011). Downsizing in a company is defined to involve the reduction of employees in a workforce. Downsizing in companies became a popular practice in the 1980s and early 1990s as it was seen as a way to deliver better shareholder value as it helps to reduce the costs of employers (downsizing, 2015). Research on downsizing in the US, UK, and Japan suggests that downsizing is being regarded by management as one of the preferred routes to help declining organizations, cutting unnecessary costs, and improve organizational performance. Usually, a layoff occurs as a cost-cutting measure. A study of 391 downsizing announcements of the S&P 100 firms for the period 1990-2006 found that layoff announcements resulted in a substantial increase in the companies’ stock prices, and that the gain was larger when the company had prior layoffs. The authors suggested that the stock price manipulation alone creates a sufficient motivation for publicly-traded corporations to adopt the practice of regular layoffs.</p>
      </div>
    </div>
  );
};

export default About;
