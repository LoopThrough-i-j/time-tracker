from typing import Final


class ResponseMessages:
    SUCCESS: Final[str] = "Success"
    FAILURE: Final[str] = "Failure"
    INVALID_ID: Final[str] = "No Data Exists with such ID"
    NOT_FOUND: Final[str] = "Document Not Found"
    NOT_FOUND_FORMATTED: Final[str] = "Document of Type {document} Not Found with ID {id}"

    # Employee
    EMPLOYEE_INVITED: Final[str] = "Employee invited successfully"
    EMPLOYEE_FOUND: Final[str] = "Employee retrieved successfully"
    EMPLOYEE_NOT_FOUND: Final[str] = "Employee not found"
    EMPLOYEE_ALREADY_EXISTS: Final[str] = "Employee with this email already exists"
