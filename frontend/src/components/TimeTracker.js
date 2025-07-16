import { useState, useEffect } from 'react';
import { Container, Row, Col, Navbar, Button } from 'react-bootstrap';
import TimerSection from './TimerSection';
import EmployeeTaskList from './EmployeeTaskList';
import SystemInfo from './SystemInfo';
import ApiService from '../services/ApiService';
import SystemInfoService from '../services/SystemInfoService';

const TimeTracker = ({ onLogout }) => {
  const [selectedTask, setSelectedTask] = useState(null);
  const [activeTimeLog, setActiveTimeLog] = useState(null);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [pollingInterval, setPollingInterval] = useState(null);

  useEffect(() => {
    setRefreshTrigger((prev) => prev + 1);
  }, []);

  useEffect(() => {
    if (activeTimeLog) {
      const interval = setInterval(() => {
        pollUpdateTimeLog(activeTimeLog.id);
      }, 10000);

      setPollingInterval(interval);

      return () => {
        if (interval) {
          clearInterval(interval);
        }
      };
    } else {
      if (pollingInterval) {
        clearInterval(pollingInterval);
        setPollingInterval(null);
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [activeTimeLog]);

  useEffect(() => {
    return () => {
      if (pollingInterval) {
        clearInterval(pollingInterval);
      }
    };
  }, [pollingInterval]);

  const pollUpdateTimeLog = async (timeLogId) => {
    try {
      await ApiService.updateTimeLog(timeLogId);
    } catch (error) {
      console.error('Error polling updateTimeLog:', error);
    }
  };

  const handleStartTimeLog = async (taskId, description) => {
    try {
      if (!selectedTask) {
        throw new Error('Please select a task first');
      }

      const systemInfo = SystemInfoService.collectSystemInfo();
      const timezoneOffset = SystemInfoService.getTimezoneOffset();
      const userName = systemInfo.user || '';

      const sysInfoPayload = {
        ...systemInfo,
        timezoneOffset,
        user: userName,
      };

      const response = await ApiService.startTimeLog(
        selectedTask.projectId,
        taskId,
        description,
        sysInfoPayload,
      );

      setActiveTimeLog(response);

      return response;
    } catch (error) {
      console.error('Error starting time log:', error);
      throw error;
    }
  };

  const handleStopTimeLog = async (timeLogId) => {
    try {
      if (pollingInterval) {
        clearInterval(pollingInterval);
        setPollingInterval(null);
      }

      const response = await ApiService.updateTimeLog(timeLogId);

      setActiveTimeLog(null);

      return response;
    } catch (error) {
      console.error('Error stopping time log:', error);
      throw error;
    }
  };

  const handleTaskSelect = (task) => {
    setSelectedTask(task);
  };

  return (
    <div>
      <Navbar
        bg="light"
        expand="lg"
        className="navbar-custom border-bottom"
      >
        <Container>
          <Navbar.Brand className="fw-bold">
            <i className="bi bi-stopwatch me-2 text-primary"></i>
						Mercor Time Tracker
          </Navbar.Brand>
          <div className="ms-auto d-flex align-items-center">
            <Button
              variant="outline-danger"
              size="sm"
              onClick={onLogout}
            >
              <i className="bi bi-box-arrow-right me-1"></i>
							Logout
            </Button>
          </div>
        </Container>
      </Navbar>
      <Container fluid className="py-4">
        <Row className="g-4">
          <Col lg={8}>
            <TimerSection
              selectedTask={selectedTask}
              activeTimeLog={activeTimeLog}
              onStartTimeLog={handleStartTimeLog}
              onStopTimeLog={handleStopTimeLog}
            />
            <div className="mt-4">
              <EmployeeTaskList
                onTaskSelect={handleTaskSelect}
                selectedTask={selectedTask}
                refreshTrigger={refreshTrigger}
              />
            </div>
          </Col>
          <Col lg={4}>
            <div className="ps-lg-3">
              <SystemInfo />
            </div>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default TimeTracker;
