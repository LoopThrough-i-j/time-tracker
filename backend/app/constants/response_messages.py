from typing import Final


class ResponseMessages:
    EMPLOYEE_NOT_FOUND: Final[str] = "Employee not found"
    EMPLOYEE_DEACTIVATED: Final[str] = "Employee deactivated successfully"
    PROJECT_NOT_FOUND: Final[str] = "Project not found"
    PROJECT_DELETED: Final[str] = "Project deleted successfully"
    PROJECT_DELETE_FAILED: Final[str] = "Failed to delete project"
    TASK_NOT_FOUND: Final[str] = "Task not found"
    TASK_DELETED: Final[str] = "Task deleted successfully"
    TASK_DELETE_FAILED: Final[str] = "Failed to delete task"
    TIME_LOG_NOT_FOUND: Final[str] = "Time log not found"
    TIME_LOG_DELETED: Final[str] = "Time log deleted successfully"
    TIME_LOG_DELETE_FAILED: Final[str] = "Failed to delete time log"
