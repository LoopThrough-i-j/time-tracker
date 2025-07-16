import { useState, useEffect } from 'react';
import { Card, Button, Form, Row, Col, Alert, Badge } from 'react-bootstrap';

const TimerSection = ({
  selectedTask,
  activeTimeLog,
  onStartTimeLog,
  onStopTimeLog,
}) => {
  const [description, setDescription] = useState('');
  const [elapsedTime, setElapsedTime] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    let interval;

    if (activeTimeLog) {
      interval = setInterval(() => {
        const startTime = new Date(activeTimeLog.startTranslated);
        const now = new Date();
        const elapsed = Math.floor((now - startTime) / 1000);

        setElapsedTime(elapsed);
      }, 1000);
    } else {
      setElapsedTime(0);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [activeTimeLog]);

  const formatTime = seconds => {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;

    return `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const handleStart = async () => {
    if (!selectedTask) {
      setError('Please select a task before starting the timer.');

      return;
    }

    setLoading(true);
    setError('');

    try {
      await onStartTimeLog(selectedTask.id, description);
      setDescription('');
    } catch (error) {
      setError(
        error.response?.data?.message ||
          'Failed to start time log. Please try again.',
      );
    } finally {
      setLoading(false);
    }
  };

  const handleStop = async () => {
    if (!activeTimeLog) return;
    setLoading(true);
    setError('');

    try {
      await onStopTimeLog(activeTimeLog.id, description);
      setDescription('');
    } catch (error) {
      setError(
        error.response?.data?.message ||
          'Failed to stop time log. Please try again.',
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Row>
        <Col>
          <Card className="time-log-card mb-4">
            <Card.Body className="text-center py-5">
              <div className="mb-4">
                <div className="timer-display display-1 fw-bold text-primary mb-2">
                  {formatTime(elapsedTime)}
                </div>
                {activeTimeLog && (
                  <Badge bg="success" className="fs-6 px-3 py-2">
                    <i
                      className="bi bi-circle-fill me-1"
                      style={{ fontSize: '0.5rem' }}
                    ></i>
                    Active Session
                  </Badge>
                )}
                {selectedTask && !activeTimeLog && (
                  <div className="mt-2">
                    <Badge bg="info" className="fs-6 px-3 py-2">
                      <i className="bi bi-check-circle me-1"></i>
                      Ready: {selectedTask.name}
                    </Badge>
                  </div>
                )}
              </div>
              {error && (
                <Alert variant="danger" className="mb-4">
                  <i className="bi bi-exclamation-triangle me-2"></i>
                  {error}
                </Alert>
              )}
              <div className="mb-4">
                <Form.Group className="mb-3">
                  <Form.Label className="fw-semibold">
                    Description (Optional)
                  </Form.Label>
                  <Form.Control
                    as="textarea"
                    rows={2}
                    placeholder="What are you working on?"
                    value={description}
                    onChange={e => setDescription(e.target.value)}
                    disabled={loading}
                  />
                </Form.Group>
              </div>
              {!activeTimeLog ? (
                <Button
                  className="start-button"
                  size="lg"
                  onClick={handleStart}
                  disabled={loading || !selectedTask}
                >
                  {loading ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2"></span>
                      Starting...
                    </>
                  ) : (
                    <>
                      <i className="bi bi-play-fill me-2"></i>
                      Start Timer
                    </>
                  )}
                </Button>
              ) : (
                <Button
                  className="stop-button"
                  size="lg"
                  onClick={handleStop}
                  disabled={loading}
                >
                  {loading ? (
                    <>
                      <span className="spinner-border spinner-border-sm me-2"></span>
                      Stopping...
                    </>
                  ) : (
                    <>
                      <i className="bi bi-stop-fill me-2"></i>
                      Stop Timer
                    </>
                  )}
                </Button>
              )}
              {!selectedTask && !activeTimeLog && (
                <div className="mt-3">
                  <small className="text-muted">
                    <i className="bi bi-info-circle me-1"></i>
                    Select a task from the Tasks tab to start tracking time
                  </small>
                </div>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
      {activeTimeLog && (
        <Row className="mt-4">
          <Col>
            <Alert variant="info" className="mb-0">
              <div className="d-flex align-items-center">
                <i className="bi bi-info-circle me-2"></i>
                <div>
                  <strong>Current Session:</strong>{' '}
                  {activeTimeLog.project?.name} - {activeTimeLog.task?.name}
                  <br />
                  <small>
                    Started at{' '}
                    {new Date(activeTimeLog.startTranslated).toLocaleString()}
                  </small>
                </div>
              </div>
            </Alert>
          </Col>
        </Row>
      )}
    </div>
  );
};

export default TimerSection;
