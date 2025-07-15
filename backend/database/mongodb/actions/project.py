from datetime import datetime

from database.mongodb.actions.base import BaseActions
from database.mongodb.models.project import Payroll, Project


class ProjectActions(BaseActions[Project]):
    def __init__(self) -> None:
        super().__init__(Project)

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
        payroll_obj = None
        if payroll:
            payroll_obj = Payroll(**payroll)

        project = Project(
            name=name,
            description=description,
            employees=employees,
            statuses=statuses,
            priorities=priorities,
            billable=billable,
            deadline=deadline,
            payroll=payroll_obj,
            creator_id=creator_id,
            organization_id=organization_id,
        )
        return self.insert_record(project)

    def get_by_name(self, name: str) -> Project | None:
        projects = self.find_records(query={"name": name}, limit=1)
        return projects[0] if projects else None
