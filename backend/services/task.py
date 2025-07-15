from datetime import datetime

from constants.exceptions import NotFoundError
from database.mongodb.actions.project import ProjectActions
from database.mongodb.actions.task import TaskActions
from database.mongodb.models.task import Task


class TaskService:
    def __init__(self):
        self.task_actions = TaskActions()
        self.project_actions = ProjectActions()

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
        project = self.project_actions.get_by_id(project_id)
        if not project:
            raise NotFoundError(f"Project with id {project_id} not found")

        created_task = self.task_actions.create_task(
            name=name,
            description=description,
            project_id=project_id,
            employees=employees,
            labels=labels,
            deadline=deadline,
            status=status,
            priority=priority,
            billable=billable if billable is not None else project.billable,
        )

        return created_task

    def get_task_by_id(self, task_id: str) -> Task | None:
        return self.task_actions.get_by_id(task_id)

    def get_all_tasks(self) -> list[Task]:
        return self.task_actions.find_records({})

    def update_task(
        self,
        task_id: str,
        name: str | None = None,
        description: str | None = None,
        project_id: str | None = None,
        employees: list[str] | None = None,
        deadline: datetime | None = None,
        status: str | None = None,
        labels: list[str] | None = None,
        priority: str | None = None,
        billable: bool | None = None,
    ) -> Task:
        update_data = {}

        if name is not None:
            update_data["name"] = name

        if description is not None:
            update_data["description"] = description

        if project_id is not None:
            update_data["project_id"] = project_id

        if employees is not None:
            update_data["employees"] = employees

        if deadline is not None:
            update_data["deadline"] = deadline

        if status is not None:
            update_data["status"] = status

        if labels is not None:
            update_data["labels"] = labels

        if priority is not None:
            update_data["priority"] = priority

        if billable is not None:
            update_data["billable"] = billable

        return self.task_actions.update_fields(task_id, update_data)

    def delete_task(self, task_id: str) -> bool:
        return self.task_actions.delete_record(task_id)
