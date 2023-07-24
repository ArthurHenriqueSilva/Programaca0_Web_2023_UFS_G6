import React from 'react';
import Dashboard from './Dashboard';
import AppSummary from './AppSummary';
import logo from './logo.png';

const App = () => {
  return (
    <div>
      <header>
        <img className="logo" src={logo} alt="Logo"></img>
      </header>
      <div className="content">
        <AppSummary />
        <div className="dashboard">
          <Dashboard />
        </div>
      </div>
    </div>
  );
};

export default App;
