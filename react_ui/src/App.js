import React, { useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, Outlet, useNavigate } from 'react-router-dom';
import './App.css';
import Login from './Login';
import Signup from './Signup';
import Home from './Home';
import refreshToken from './refresh';

const isAuthenticated = () => {
  const authToken = localStorage.getItem('_a');
  return authToken !== null;
};

const PrivateWrapper = ({ children }) => {
  const navigate = useNavigate();

  const checkToken = async () => {
    const tokenExpired = !isAuthenticated();

    if (tokenExpired) {
      try {
        await refreshToken();
      } catch (error) {
        navigate('/login/');
      }
    }
  };

  useEffect(() => {
    const setupTokenRefreshTimer = async () => {
      // Initial check when the component mounts
      await checkToken();

      // Set up a timer to refresh the token every 4 minutes
      const timerId = setInterval(async () => {
        await checkToken();
      }, 4 * 60 * 1000);

      // Clean up the timer when the component is unmounted
      return () => {
        clearInterval(timerId);
      };
    };

    // Call the setup function
    setupTokenRefreshTimer();

    // Include checkToken in the dependency array
  }, );

  return isAuthenticated() ? <Outlet>{children}</Outlet> : <Navigate to="/login" replace />;
};

function App() {
  return (
    <Router>
      <Routes>
        <Route
          exact
          path="/login"
          element={isAuthenticated() ? <Navigate to="/" replace /> : <Login />}
        />
        <Route exact path="/signup" element={<Signup />} />
        <Route element={<PrivateWrapper />}>
          <Route path="/" element={<Home />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
