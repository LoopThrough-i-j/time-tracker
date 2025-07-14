from datetime import datetime, timezone

from constants.exceptions import BadRequestError
from database.mongodb.actions.employee import EmployeeActions
from database.mongodb.models.employee import Employee, EmployeeType


class EmployeeService:
    def __init__(self) -> None:
        self.employee_actions = EmployeeActions()

    def invite_employee(self, name: str, email: str, team_id: str) -> Employee:
        existing_employee = self.employee_actions.get_by_email(email)
        if existing_employee:
            raise BadRequestError("Employee with this email already exists")

        invited_datetime = datetime.now(timezone.utc)

        employee = self.employee_actions.create_employee(
            name=name,
            email=email,
            team_id=team_id,
            identifier=email,
            invited_at=invited_datetime,
            type=EmployeeType.PERSONAL,
        )

        return employee

    def get_employee_by_id(self, employee_id: str) -> Employee | None:
        return self.employee_actions.get_by_id(employee_id)

    def get_employees_by_team(self, team_id: str) -> list[Employee]:
        return self.employee_actions.get_by_team_id(team_id)

    def get_all_employees(self) -> list[Employee]:
        return self.employee_actions.find_records(query={})

    def update_employee(self, employee_id: str, name: str, email: str, team_id: str, projects: list[str]) -> Employee:
        existing_employee = self.employee_actions.get_by_id(employee_id)
        if not existing_employee:
            raise BadRequestError("Employee not found")

        if existing_employee.email != email:
            employee_with_email = self.employee_actions.get_by_email(email)
            if employee_with_email and employee_with_email.id != employee_id:
                raise BadRequestError("Employee with this email already exists")

        existing_employee.name = name
        existing_employee.email = email
        existing_employee.team_id = team_id
        existing_employee.projects = projects

        updated_employee = self.employee_actions.update_document(existing_employee)
        return updated_employee

    def deactivate_employee(self, employee_id: str) -> Employee:
        existing_employee = self.employee_actions.get_by_id(employee_id)
        if not existing_employee:
            raise BadRequestError("Employee not found")

        existing_employee.is_active = False

        updated_employee = self.employee_actions.update_document(existing_employee)
        return updated_employee
