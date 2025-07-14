from datetime import datetime

from database.mongodb.actions.base import BaseActions
from database.mongodb.models.task import Task


class TaskActions(BaseActions[Task]):
    def __init__(self) -> None:
        super().__init__(Task)

    def create_task(
        self,
        name: str,
        description: str,
        project_id: str,
        employees: list[str] = [],
        labels: list[str] = [],
        deadline: datetime | None = None,
        status: str | None = None,
        priority: str | None = None,
        billable: bool | None = None,
    ) -> Task:

        task = Task(
            name=name,
            description=description,
            employees=employees,
            project_id=project_id,
            deadline=deadline,
            status=status,
            labels=labels,
            priority=priority,
            billable=billable,
        )
        return self.insert_record(task)
