from datetime import datetime

from constants.exceptions import BadRequestError
from database.mongodb.actions.employee import EmployeeActions
from database.mongodb.actions.project import ProjectActions
from database.mongodb.models.project import Project


class ProjectService:
    def __init__(self) -> None:
        self.project_actions = ProjectActions()
        self.employee_actions = EmployeeActions()

    def create_project(
        self,
        name: str,
        description: str,
        employees: list[str],
        statuses: list[str],
        priorities: list[str],
        billable: bool,
        deadline: datetime | None = None,
        payroll: dict | None = None,
        creator_id: str = "default-creator",
        organization_id: str = "default-org",
    ) -> Project:
        existing_project = self.project_actions.get_by_name(name)
        if existing_project:
            raise BadRequestError("Project with this name already exists")

        if employees:
            found_employees = self.employee_actions.find_records(query={"_id": {"$in": employees}})
            found_employee_ids = {emp.id for emp in found_employees}
            missing_employees = set(employees) - found_employee_ids
            if missing_employees:
                raise BadRequestError(f"Employees not found: {', '.join(missing_employees)}")

        project = self.project_actions.create_project(
            name=name,
            description=description,
            employees=employees,
            statuses=statuses,
            priorities=priorities,
            billable=billable,
            deadline=deadline,
            payroll=payroll,
            creator_id=creator_id,
            organization_id=organization_id,
        )

        if employees:
            self.employee_actions.bulk_add_to_set(employees, "projects", project.id)

        return project

    def get_project_by_id(self, project_id: str) -> Project | None:
        return self.project_actions.get_by_id(project_id)

    def get_all_projects(self) -> list[Project]:
        return self.project_actions.find_records(query={})

    def update_project(
        self,
        project_id: str,
        name: str | None = None,
        description: str | None = None,
        employees: list[str] | None = None,
        statuses: list[str] | None = None,
        priorities: list[str] | None = None,
        billable: bool | None = None,
        deadline: datetime | None = None,
        payroll: dict | None = None,
    ) -> Project:
        existing_project = self.project_actions.get_by_id(project_id)
        if not existing_project:
            raise BadRequestError("Project not found")

        if name is not None and existing_project.name != name:
            project_with_name = self.project_actions.get_by_name(name)
            if project_with_name:
                raise BadRequestError("Project with this name already exists")

        update_data = {}

        if name is not None:
            update_data["name"] = name
        if description is not None:
            update_data["description"] = description
        if statuses is not None:
            update_data["statuses"] = statuses
        if priorities is not None:
            update_data["priorities"] = priorities
        if billable is not None:
            update_data["billable"] = billable
        if deadline is not None:
            update_data["deadline"] = deadline
        if payroll is not None:
            update_data["payroll"] = payroll

        if employees is not None:
            if employees:
                found_employees = self.employee_actions.find_records(query={"_id": {"$in": employees}})
                found_employee_ids = {emp.id for emp in found_employees}
                missing_employees = set(employees) - found_employee_ids
                if missing_employees:
                    raise BadRequestError(f"Employees not found: {', '.join(missing_employees)}")

            update_data["employees"] = employees
            old_employees = set(existing_project.employees)
            new_employees = set(employees)
            employees_to_add = list(new_employees - old_employees)
            employees_to_remove = list(old_employees - new_employees)
        else:
            employees_to_add = []
            employees_to_remove = []

        updated_project = self.project_actions.update_fields(project_id, update_data)

        if employees_to_add:
            self.employee_actions.bulk_add_to_set(employees_to_add, "projects", [project_id])

        if employees_to_remove:
            self.employee_actions.bulk_pull(employees_to_remove, "projects", [project_id])

        return updated_project

    def delete_project(self, project_id: str) -> bool:
        existing_project = self.project_actions.get_by_id(project_id)
        if not existing_project:
            raise BadRequestError("Project not found")

        if existing_project.employees:
            self.employee_actions.bulk_pull(existing_project.employees, "projects", [project_id])

        return self.project_actions.delete_record(project_id, soft_delete=True)
