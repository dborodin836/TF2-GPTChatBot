import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter, HashRouter } from 'react-router-dom';
import { ThemeProvider } from '@material-tailwind/react';
import { AlertProvider } from './components/AlertContext';

const Router = 'true' === 'true' ? HashRouter : BrowserRouter;

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <ThemeProvider>
      <Router>
        <AlertProvider>
          <App />
        </AlertProvider>
      </Router>
    </ThemeProvider>
  </React.StrictMode>,
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
