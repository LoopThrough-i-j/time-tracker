import os
import time

BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8080")
API_BASE_URL = f"{BASE_URL}/api/v1"

HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

TIMESTAMP = int(time.time())

TEST_DATA = {
    "employee": {"name": "Test Employee", "email": f"test{TIMESTAMP}@example.com", "teamId": "test-team-001"},
    "project": {
        "name": f"Test Project {TIMESTAMP}",
        "description": "A test project for API validation",
        "statuses": ["To Do", "In progress", "Done"],
        "priorities": ["low", "medium", "high"],
        "billable": True,
        "payroll": {"billRate": 25.0, "overtimeBillrate": 55.0},
    },
    "task": {
        "name": f"Test Task {TIMESTAMP}",
        "description": "A test task for API validation",
        "status": "todo",
        "priority": "medium",
        "billable": True,
    },
    "auth": {"password": "TestPassword123!"},
}
