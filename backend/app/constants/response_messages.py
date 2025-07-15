from typing import Final


class ResponseMessages:
    EMPLOYEE_NOT_FOUND: Final[str] = "Employee not found"
    EMPLOYEE_DEACTIVATED: Final[str] = "Employee deactivated successfully"
    EMPLOYEE_ALREADY_SIGNED_UP: Final[str] = "Employee has already signed up"
    PROJECT_NOT_FOUND: Final[str] = "Project not found"
    PROJECT_DELETED: Final[str] = "Project deleted successfully"
    PROJECT_DELETE_FAILED: Final[str] = "Failed to delete project"
    TASK_NOT_FOUND: Final[str] = "Task not found"
    TASK_DELETED: Final[str] = "Task deleted successfully"
    TASK_DELETE_FAILED: Final[str] = "Failed to delete task"
    TIME_LOG_NOT_FOUND: Final[str] = "Time log not found"
    TIME_LOG_ALREADY_ACTIVE: Final[str] = "Cannot start a new time log while another is already active"
    TIME_LOG_DELETED: Final[str] = "Time log deleted successfully"
    TIME_LOG_DELETE_FAILED: Final[str] = "Failed to delete time log"
    INVALID_SIGNUP_LINK: Final[str] = "Invalid signup link"
    INVALID_SIGNUP_LINK_FOR_EMAIL: Final[str] = "Invalid signup link for this email address"
    UNEXPECTED_ERROR: Final[str] = "An unexpected error occurred. Please try again."
    INVALID_TOKEN_EMPLOYEE_ID_NOT_FOUND: Final[str] = "Invalid token: employee_id not found"
