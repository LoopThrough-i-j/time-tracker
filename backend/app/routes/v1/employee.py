from fastapi import APIRouter, Depends

from app.constants.response_messages import ResponseMessages
from app.dependencies.auth import get_current_employee_id
from app.dto.request.v1.employee import EmployeeInviteRequest, EmployeeUpdateRequest
from app.dto.response.v1.employee import EmployeeData
from app.dto.response.v1.task import TaskResponse
from app.tags import APITags

from constants.exceptions import NotFoundError
from services.employee import EmployeeService
from services.task import TaskService

employee_router = APIRouter(prefix="/employee", tags=[APITags.EMPLOYEE.name])


@employee_router.get("/", response_model=list[EmployeeData])
async def list_employees() -> list[EmployeeData]:
    employee_service = EmployeeService()

    employees = employee_service.get_all_employees()

    employee_list = []
    for employee in employees:
        invited_timestamp = int(employee.invited_at.timestamp() * 1000)
        created_at_timestamp = int(employee.created_at.timestamp() * 1000)

        employee_data = EmployeeData(
            id=employee.id,
            name=employee.name,
            email=employee.email,
            team_id=employee.team_id,
            identifier=employee.identifier,
            type=employee.type.value,
            projects=employee.projects,
            deactivated=0 if employee.is_active else 1,
            invited=invited_timestamp,
            created_at=created_at_timestamp,
        )
        employee_list.append(employee_data)

    return employee_list


@employee_router.post("/", response_model=EmployeeData)
async def invite_employee(request_data: EmployeeInviteRequest) -> EmployeeData:
    employee_service = EmployeeService()

    employee = employee_service.invite_employee(
        name=request_data.name, email=request_data.email, team_id=request_data.team_id
    )

    invited_timestamp = int(employee.invited_at.timestamp() * 1000)
    created_at_timestamp = int(employee.created_at.timestamp() * 1000)

    return EmployeeData(
        id=employee.id,
        name=employee.name,
        email=employee.email,
        team_id=employee.team_id,
        identifier=employee.identifier,
        type=employee.type.value,
        projects=employee.projects,
        deactivated=0 if employee.is_active else 1,
        invited=invited_timestamp,
        created_at=created_at_timestamp,
    )


@employee_router.put("/{emp_id}", response_model=EmployeeData)
async def update_employee(emp_id: str, request_data: EmployeeUpdateRequest) -> EmployeeData:
    employee_service = EmployeeService()

    employee = employee_service.update_employee(
        employee_id=emp_id,
        name=request_data.name,
        email=request_data.email,
        team_id=request_data.team_id,
        projects=request_data.projects,
    )

    invited_timestamp = int(employee.invited_at.timestamp() * 1000)
    created_at_timestamp = int(employee.created_at.timestamp() * 1000)

    return EmployeeData(
        id=employee.id,
        name=employee.name,
        email=employee.email,
        team_id=employee.team_id,
        identifier=employee.identifier,
        type=employee.type.value,
        projects=employee.projects,
        deactivated=0 if employee.is_active else 1,
        invited=invited_timestamp,
        created_at=created_at_timestamp,
    )


@employee_router.get("/tasks", response_model=list[TaskResponse])
async def get_employee_tasks(employee_id: str = Depends(get_current_employee_id)) -> list[TaskResponse]:
    """Get all tasks assigned to the authenticated employee"""
    task_service = TaskService()

    print(f"DEBUG: Getting tasks for employee_id: {employee_id}")

    # Get tasks assigned to the employee
    tasks = task_service.get_tasks_by_employee(employee_id)

    print(f"DEBUG: Found {len(tasks)} tasks for employee {employee_id}")

    task_responses = []
    for task in tasks:
        print(f"DEBUG: Processing task {task.id} with employees: {task.employees}")
        created_at_timestamp = int(task.created_at.timestamp() * 1000)
        updated_at_timestamp = int(task.updated_at.timestamp() * 1000)

        deadline_timestamp = None
        if task.deadline:
            deadline_timestamp = int(task.deadline.timestamp() * 1000)

        task_responses.append(
            TaskResponse(
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
        )

    print(f"DEBUG: Returning {len(task_responses)} task responses")
    return task_responses


@employee_router.get("/{emp_id}", response_model=EmployeeData)
async def get_employee(emp_id: str) -> EmployeeData:
    employee_service = EmployeeService()

    employee = employee_service.get_employee_by_id(emp_id)

    if not employee:
        raise NotFoundError(ResponseMessages.EMPLOYEE_NOT_FOUND)

    invited_timestamp = int(employee.invited_at.timestamp() * 1000)
    created_at_timestamp = int(employee.created_at.timestamp() * 1000)

    return EmployeeData(
        id=employee.id,
        name=employee.name,
        email=employee.email,
        team_id=employee.team_id,
        identifier=employee.identifier,
        type=employee.type.value,
        projects=employee.projects,
        deactivated=0 if employee.is_active else 1,
        invited=invited_timestamp,
        created_at=created_at_timestamp,
    )


@employee_router.get("/deactivate/{emp_id}")
async def deactivate_employee(emp_id: str) -> dict[str, str]:
    employee_service = EmployeeService()

    employee_service.deactivate_employee(emp_id)

    return {"message": ResponseMessages.EMPLOYEE_DEACTIVATED}
