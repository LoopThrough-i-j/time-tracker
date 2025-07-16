import { useState, useEffect } from 'react';
import {
  Card,
  Badge,
  Form,
  InputGroup,
  Spinner,
  Alert,
  Button,
} from 'react-bootstrap';
import ApiService from '../services/ApiService';

const EmployeeTaskList = ({ onTaskSelect, selectedTask, refreshTrigger }) => {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadTasks();
  }, []);

  useEffect(() => {
    if (refreshTrigger) {
      loadTasks();
    }
  }, [refreshTrigger]);

  const loadTasks = async () => {
    setLoading(true);
    setError(null);

    try {
      const tasksData = await ApiService.getEmployeeTasks();

      if (Array.isArray(tasksData)) {
        setTasks(tasksData);
      } else {
        setTasks([]);
      }
    } catch (error) {
      console.error('Error loading tasks:', error);
      let errorMessage = 'Failed to load tasks';

      if (error.response?.status === 401 || error.response?.status === 403) {
        errorMessage = 'Authentication failed. Please log in again.';
        await ApiService.logout();
      } else if (error.response?.data?.detail) {
        errorMessage = error.response.data.detail;
      } else if (error.message) {
        errorMessage = error.message;
      }

      setError(errorMessage);
      setTasks([]);
    } finally {
      setLoading(false);
    }
  };

  const getProjectName = projectId => {
    const task = tasks.find(t => t.project_id === projectId);

    return task?.project_name || `Project ${projectId}`;
  };

  const filteredTasks = tasks.filter(task => {
    return (
      task.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (task.description &&
        task.description.toLowerCase().includes(searchTerm.toLowerCase()))
    );
  });

  if (loading) {
    return (
      <Card>
        <Card.Body className="text-center py-5">
          <Spinner animation="border" className="me-2" />
          Loading your tasks...
        </Card.Body>
      </Card>
    );
  }

  if (error) {
    return (
      <Card>
        <Card.Body>
          <Alert variant="danger">
            <i className="bi bi-exclamation-triangle me-2"></i>
            {error}
            <Button
              variant="outline-danger"
              size="sm"
              className="ms-2"
              onClick={loadTasks}
            >
              <i className="bi bi-arrow-clockwise"></i>
            </Button>
          </Alert>
        </Card.Body>
      </Card>
    );
  }

  return (
    <Card>
      <Card.Header className="d-flex justify-content-between align-items-center">
        <h5 className="mb-0">
          <i className="bi bi-list-task me-2"></i>
          Select a Task
        </h5>
        <Button variant="outline-secondary" size="sm" onClick={loadTasks}>
          <i className="bi bi-arrow-clockwise"></i>
        </Button>
      </Card.Header>
      <Card.Body>

        <InputGroup className="mb-3">
          <InputGroup.Text>
            <i className="bi bi-search"></i>
          </InputGroup.Text>
          <Form.Control
            type="text"
            placeholder="Search tasks..."
            value={searchTerm}
            onChange={e => setSearchTerm(e.target.value)}
          />
        </InputGroup>

        {filteredTasks.length === 0 ? (
          <div className="text-center py-4">
            <i className="bi bi-list-ul display-4 text-muted"></i>
            <p className="text-muted mt-2">
              {tasks.length === 0 ? 'No tasks assigned' : 'No tasks found'}
            </p>
          </div>
        ) : (
          <div
            className="task-list"
            style={{ maxHeight: '400px', overflowY: 'auto' }}
          >
            {filteredTasks.map(task => (
              <div
                key={task.id}
                className={`p-3 border-2 rounded mb-2 cursor-pointer shadow-sm ${
                  selectedTask?.id === task.id
                    ? 'border-primary bg-primary bg-opacity-10 shadow'
                    : 'border-secondary bg-white'
                }`}
                onClick={() => onTaskSelect(task)}
                style={{
                  cursor: 'pointer',
                  transition: 'all 0.2s ease',
                  outline:
                    selectedTask?.id === task.id
                      ? '2px solid var(--bs-primary)'
                      : '1px solid #dee2e6',
                  outlineOffset: '2px',
                }}
              >
                <div className="d-flex justify-content-between align-items-start">
                  <div className="flex-grow-1">
                    <h6 className="mb-1">{task.name}</h6>
                    <small className="text-muted">
                      <i className="bi bi-folder me-1"></i>
                      {getProjectName(task.project_id)}
                    </small>
                    {task.description && (
                      <p className="text-muted small mb-1 mt-1">
                        {task.description.length > 80
                          ? `${task.description.substring(0, 80)}...`
                          : task.description}
                      </p>
                    )}
                  </div>
                  <div className="text-end">
                    {task.status && (
                      <Badge bg="secondary" className="small">
                        {task.status}
                      </Badge>
                    )}
                    {task.estimated_hours && (
                      <div className="mt-1">
                        <small className="text-muted">
                          <i className="bi bi-clock me-1"></i>
                          {task.estimated_hours}h
                        </small>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
        <div className="mt-3 text-center">
          <small className="text-muted">
            {filteredTasks.length} of {tasks.length} tasks
          </small>
        </div>
      </Card.Body>
    </Card>
  );
};

export default EmployeeTaskList;
