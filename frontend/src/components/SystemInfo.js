import { useState, useEffect } from 'react';
import { Card, ListGroup, Badge } from 'react-bootstrap';
import SystemInfoService from '../services/SystemInfoService';

const SystemInfo = () => {
  const [systemInfo, setSystemInfo] = useState({});

  useEffect(() => {
    gatherSystemInfo();
  }, []);

  const gatherSystemInfo = () => {
    const info = SystemInfoService.collectSystemInfo();

    setSystemInfo(info);
  };

  return (
		<div>
			<Card className="system-info mb-4">
				<Card.Header>
					<h5 className="mb-0">
						<i className="bi bi-laptop me-2"></i>
						System Information
					</h5>
				</Card.Header>
				<ListGroup variant="flush">
					<ListGroup.Item className="d-flex justify-content-between align-items-center">
						<span>
							<i className="bi bi-person me-2 text-muted"></i>
							User
						</span>
						<Badge bg="primary">{systemInfo.user}</Badge>
					</ListGroup.Item>
					<ListGroup.Item className="d-flex justify-content-between align-items-center">
						<span>
							<i className="bi bi-pc-display me-2 text-muted"></i>
							Computer
						</span>
						<Badge bg="primary">{systemInfo.computer}</Badge>
					</ListGroup.Item>
					<ListGroup.Item className="d-flex justify-content-between align-items-center">
						<span>
							<i className="bi bi-building me-2 text-muted"></i>
							Domain
						</span>
						<Badge bg="primary">{systemInfo.domain}</Badge>
					</ListGroup.Item>
					<ListGroup.Item className="d-flex justify-content-between align-items-center">
						<span>
							<i className="bi bi-person-badge me-2 text-muted"></i>
							Name
						</span>
						<Badge bg="primary">{systemInfo.name}</Badge>
					</ListGroup.Item>
					<ListGroup.Item className="d-flex justify-content-between align-items-center">
						<span>
							<i className="bi bi-fingerprint me-2 text-muted"></i>
							HWID
						</span>
						<Badge bg="primary">{systemInfo.hwid}</Badge>
					</ListGroup.Item>
					<ListGroup.Item className="d-flex justify-content-between align-items-center">
						<span>
							<i className="bi bi-laptop me-2 text-muted"></i>
							OS
						</span>
						<Badge bg="primary">{systemInfo.os}</Badge>
					</ListGroup.Item>
					<ListGroup.Item className="d-flex justify-content-between align-items-center">
						<span>
							<i className="bi bi-info-circle me-2 text-muted"></i>
							OS Version
						</span>
						<Badge bg="primary">{systemInfo.osVersion}</Badge>
					</ListGroup.Item>
				</ListGroup>
			</Card>
		</div>
  );
};

export default SystemInfo;
