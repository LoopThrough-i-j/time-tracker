import { useState, useEffect } from 'react';
import { Container } from 'react-bootstrap';
import AuthComponent from './components/AuthComponent';
import TimeTracker from './components/TimeTracker';
import ApiService from './services/ApiService';
import 'bootstrap/dist/css/bootstrap.min.css';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      if (ApiService.isAuthenticated()) {
        setIsAuthenticated(true);
      }
    } catch (error) {
      console.error('Error checking auth status:', error);
      await ApiService.logout();
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = () => {
    setIsAuthenticated(true);
  };

  const handleLogout = async () => {
    await ApiService.logout();
    setIsAuthenticated(false);
  };

  if (loading) {
    return (
      <Container
        className="d-flex justify-content-center align-items-center"
        style={{ height: '100vh' }}
      >
        <div className="text-center">
          <div className="spinner-border text-primary" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
          <p className="mt-3">Loading Mercor Time Tracker...</p>
        </div>
      </Container>
    );
  }

  return (
    <div className="App">
      {!isAuthenticated ? (
        <AuthComponent onLogin={handleLogin} />
      ) : (
        <TimeTracker onLogout={handleLogout} />
      )}
    </div>
  );
}

export default App;
