from datetime import datetime

from fastapi import APIRouter

from app.constants.response_messages import ResponseMessages
from app.dto.request.v1.task import CreateTaskRequest, UpdateTaskRequest
from app.dto.response.v1.task import TaskResponse
from app.tags import APITags

from services.task import TaskService

task_router = APIRouter(prefix="/task", tags=[APITags.TASK.name])


@task_router.get("/", response_model=list[TaskResponse])
def list_tasks() -> list[TaskResponse]:
    task_service = TaskService()

    tasks = task_service.get_all_tasks()

    return [
        TaskResponse(
            id=task.id,
            name=task.name,
            description=task.description,
            employees=task.employees,
            project_id=task.project_id,
            deadline=int(task.deadline.timestamp() * 1000) if task.deadline else None,
            status=task.status,
            labels=task.labels,
            priority=task.priority,
            billable=task.billable,
            created_at=int(task.created_at.timestamp() * 1000),
            updated_at=int(task.updated_at.timestamp() * 1000),
        )
        for task in tasks
    ]


@task_router.post("/", response_model=TaskResponse)
def create_task(request_data: CreateTaskRequest) -> TaskResponse:
    task_service = TaskService()

    deadline_datetime = None
    if request_data.deadline:
        deadline_datetime = datetime.fromtimestamp(request_data.deadline / 1000)

    task = task_service.create_task(
        name=request_data.name,
        description=request_data.description,
        project_id=request_data.project_id,
        employees=request_data.employees,
        deadline=deadline_datetime,
        status=request_data.status,
        labels=request_data.labels,
        priority=request_data.priority,
        billable=request_data.billable,
    )

    created_at_timestamp = int(task.created_at.timestamp() * 1000)
    updated_at_timestamp = int(task.updated_at.timestamp() * 1000)

    deadline_timestamp = None
    if task.deadline:
        deadline_timestamp = int(task.deadline.timestamp() * 1000)

    return TaskResponse(
        id=task.id,
        name=task.name,
        description=task.description,
        employees=task.employees,
        project_id=task.project_id,
        deadline=deadline_timestamp,
        status=task.status,
        labels=task.labels,
        priority=task.priority,
        billable=task.billable,
        created_at=created_at_timestamp,
        updated_at=updated_at_timestamp,
    )


@task_router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: str) -> TaskResponse:
    task_service = TaskService()

    task = task_service.get_task_by_id(task_id)

    created_at_timestamp = int(task.created_at.timestamp() * 1000)
    updated_at_timestamp = int(task.updated_at.timestamp() * 1000)

    deadline_timestamp = None
    if task.deadline:
        deadline_timestamp = int(task.deadline.timestamp() * 1000)

    return TaskResponse(
        id=task.id,
        name=task.name,
        description=task.description,
        employees=task.employees,
        project_id=task.project_id,
        deadline=deadline_timestamp,
        status=task.status,
        labels=task.labels,
        priority=task.priority,
        billable=task.billable,
        created_at=created_at_timestamp,
        updated_at=updated_at_timestamp,
    )


@task_router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: str, request_data: UpdateTaskRequest) -> TaskResponse:
    task_service = TaskService()

    deadline_datetime = None
    if request_data.deadline:
        deadline_datetime = datetime.fromtimestamp(request_data.deadline / 1000)

    task = task_service.update_task(
        task_id=task_id,
        name=request_data.name,
        description=request_data.description,
        project_id=request_data.project_id,
        employees=request_data.employees,
        deadline=deadline_datetime,
        status=request_data.status,
        labels=request_data.labels,
        priority=request_data.priority,
        billable=request_data.billable,
    )

    created_at_timestamp = int(task.created_at.timestamp() * 1000)
    updated_at_timestamp = int(task.updated_at.timestamp() * 1000)

    deadline_timestamp = None
    if task.deadline:
        deadline_timestamp = int(task.deadline.timestamp() * 1000)

    return TaskResponse(
        id=task.id,
        name=task.name,
        description=task.description,
        employees=task.employees,
        project_id=task.project_id,
        deadline=deadline_timestamp,
        status=task.status,
        labels=task.labels,
        priority=task.priority,
        billable=task.billable,
        created_at=created_at_timestamp,
        updated_at=updated_at_timestamp,
    )


@task_router.delete("/{task_id}")
def delete_task(task_id: str) -> dict[str, str]:
    task_service = TaskService()

    success = task_service.delete_task(task_id)

    if success:
        return {"message": ResponseMessages.TASK_DELETED}
    else:
        return {"message": ResponseMessages.TASK_DELETE_FAILED}
