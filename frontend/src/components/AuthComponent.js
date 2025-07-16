import { useState } from 'react';
import {
  Container,
  Row,
  Col,
  Card,
  Form,
  Button,
  Alert,
  Navbar,
} from 'react-bootstrap';
import ApiService from '../services/ApiService';

const AuthComponent = ({ onLogin }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async e => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await ApiService.login(email, password);

      if (!response.access_token) {
        throw new Error('No access token received from server');
      }

      onLogin();
    } catch (error) {
      console.error('Login error:', error);
      let errorMessage = 'Login failed. Please try again.';

      if (error.code === 'ERR_NETWORK') {
        errorMessage =
          'Cannot connect to server. Please check if the backend is running on port 8080.';
      } else if (error.message?.includes('CORS')) {
        errorMessage =
          'Connection blocked by CORS policy. Please check the backend CORS configuration.';
      } else if (error.response?.status === 0) {
        errorMessage =
          'Cannot reach the server. Please check your network connection and ensure the backend is running.';
      } else if (error.response?.data?.message) {
        errorMessage = error.response.data.message;
      } else if (error.response?.status === 401) {
        errorMessage =
          'Invalid email or password. Please check your credentials.';
      } else if (error.response?.status === 400) {
        errorMessage =
          error.response?.data?.message ||
          'Invalid credentials or account not set up.';
      } else if (error.response?.status === 500) {
        errorMessage = 'Server error. Please contact your administrator.';
      } else if (error.message) {
        errorMessage = error.message;
      }

      setError(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Navbar className="navbar-custom">
        <Container>
          <Navbar.Brand className="fw-bold">
            <i className="bi bi-stopwatch me-2"></i>
						Mercor Time Tracker
          </Navbar.Brand>
        </Container>
      </Navbar>
      <Container
        className="d-flex align-items-center justify-content-center px-3"
        style={{ minHeight: '90vh' }}
      >
        <Row className="w-100 justify-content-center">
          <Col
            xs={12}
            sm={10}
            md={8}
            lg={6}
            xl={4}
            className="mx-auto"
          >
            <Card className="shadow-lg border-0">
              <Card.Body className="p-5">
                <div className="text-center mb-4">
                  <div
                    className="app-header rounded-circle d-inline-flex align-items-center justify-content-center mb-3"
                    style={{
                      width: '80px',
                      height: '80px',
                    }}
                  >
                    <i className="bi bi-stopwatch fs-1"></i>
                  </div>
                  <h2 className="fw-bold text-dark">
										Welcome Back
                  </h2>
                  <p className="text-muted">
										Sign in to start tracking your time
                  </p>
                </div>
                {error && (
                  <Alert
                    variant="danger"
                    className="d-flex align-items-center"
                  >
                    <i className="bi bi-exclamation-triangle me-2"></i>
                    {error}
                  </Alert>
                )}
                <Form onSubmit={handleSubmit}>
                  <Form.Group className="mb-3">
                    <Form.Label className="fw-semibold">
											Email Address
                    </Form.Label>
                    <Form.Control
                      type="email"
                      placeholder="Enter your email"
                      value={email}
                      onChange={(e) =>
                        setEmail(e.target.value)
                      }
                      required
                      size="lg"
                      className="border-2"
                    />
                  </Form.Group>
                  <Form.Group className="mb-4">
                    <Form.Label className="fw-semibold">
											Password
                    </Form.Label>
                    <Form.Control
                      type="password"
                      placeholder="Enter your password"
                      value={password}
                      onChange={(e) =>
                        setPassword(e.target.value)
                      }
                      required
                      size="lg"
                      className="border-2"
                    />
                  </Form.Group>
                  <Button
                    type="submit"
                    variant="primary"
                    size="lg"
                    disabled={loading}
                    className="w-100 fw-semibold"
                    style={{
                      background:
												'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                      border: 'none',
                      borderRadius: '12px',
                    }}
                  >
                    {loading ? (
                      <>
                        <span
                          className="spinner-border spinner-border-sm me-2"
                          role="status"
                        ></span>
												Signing In...
                      </>
                    ) : (
                      <>
                        <i className="bi bi-box-arrow-in-right me-2"></i>
												Sign In
                      </>
                    )}
                  </Button>
                </Form>
                <div className="text-center mt-4">
                  <small className="text-muted">
										Secure time tracking for Mercor
										employees
                  </small>
                </div>
              </Card.Body>
            </Card>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default AuthComponent;
