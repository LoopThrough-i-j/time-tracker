from datetime import datetime, timezone

from constants.exceptions import BadRequestError
from database.mongodb.actions.employee import EmployeeActions
from database.mongodb.actions.project import ProjectActions
from database.mongodb.models.employee import Employee, EmployeeType


class EmployeeService:
    def __init__(self) -> None:
        self.employee_actions = EmployeeActions()
        self.project_actions = ProjectActions()

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

    def update_employee(
        self,
        employee_id: str,
        name: str | None = None,
        email: str | None = None,
        team_id: str | None = None,
        projects: list[str] | None = None,
    ) -> Employee:
        existing_employee = self.employee_actions.get_by_id(employee_id)
        if not existing_employee:
            raise BadRequestError("Employee not found")

        update_data = {}

        if name is not None:
            update_data["name"] = name

        if email is not None:
            update_data["email"] = email

        if team_id is not None:
            update_data["team_id"] = team_id

        if projects is not None:
            update_data["projects"] = projects
            old_projects = set(existing_employee.projects)
            new_projects = set(projects)
            projects_to_add = list(new_projects - old_projects)
            projects_to_remove = list(old_projects - new_projects)
        else:
            projects_to_add = []
            projects_to_remove = []

        updated_employee = self.employee_actions.update_fields(employee_id, update_data)

        if projects_to_add:
            self.project_actions.bulk_add_to_set(projects_to_add, "employees", [employee_id])

        if projects_to_remove:
            self.project_actions.bulk_pull(projects_to_remove, "employees", [employee_id])

        return updated_employee

    def deactivate_employee(self, employee_id: str) -> Employee:
        existing_employee = self.employee_actions.get_by_id(employee_id)
        if not existing_employee:
            raise BadRequestError("Employee not found")

        updated_employee = self.employee_actions.update_fields(employee_id, {"is_active": False, "projects": []})

        if existing_employee.projects:
            self.project_actions.bulk_pull(existing_employee.projects, "employees", [employee_id])

        return updated_employee
