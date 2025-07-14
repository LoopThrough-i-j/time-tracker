from datetime import datetime

from fastapi import APIRouter

from app.constants.response_messages import ResponseMessages
from app.dto.request.v1.project import ProjectCreateRequest, ProjectUpdateRequest
from app.dto.response.v1.project import PayrollData, ProjectData
from app.tags import APITags

from constants.exceptions import NotFoundError
from services.project import ProjectService

project_router = APIRouter(prefix="/project", tags=[APITags.PROJECT.name])


@project_router.post("/", response_model=ProjectData)
async def create_project(request_data: ProjectCreateRequest) -> ProjectData:
    project_service = ProjectService()

    payroll_dict = None
    if request_data.payroll:
        payroll_dict = {
            "bill_rate": request_data.payroll.billRate,
            "overtime_billrate": request_data.payroll.overtimeBillrate,
        }

    deadline_datetime = None
    if request_data.deadline:
        deadline_datetime = datetime.fromtimestamp(request_data.deadline / 1000)

    project = project_service.create_project(
        name=request_data.name,
        description=request_data.description,
        employees=request_data.employees,
        statuses=request_data.statuses,
        priorities=request_data.priorities,
        billable=request_data.billable,
        deadline=deadline_datetime,
        payroll=payroll_dict,
    )

    created_at_timestamp = int(project.created_at.timestamp() * 1000)

    payroll_data = None
    if project.payroll:
        payroll_data = PayrollData(
            billRate=project.payroll.bill_rate,
            overtimeBillrate=project.payroll.overtime_billrate,
        )

    return ProjectData(
        id=project.id,
        name=project.name,
        description=project.description,
        employees=project.employees,
        statuses=project.statuses,
        priorities=project.priorities,
        billable=project.billable,
        deadline=int(project.deadline.timestamp() * 1000) if project.deadline else None,
        payroll=payroll_data,
        archived=project.archived,
        creatorId=project.creator_id,
        organizationId=project.organization_id,
        teams=project.teams,
        createdAt=created_at_timestamp,
    )


@project_router.get("/", response_model=list[ProjectData])
async def list_projects() -> list[ProjectData]:
    project_service = ProjectService()

    projects = project_service.get_all_projects()

    project_list = []
    for project in projects:
        created_at_timestamp = int(project.created_at.timestamp() * 1000)

        payroll_data = None
        if project.payroll:
            payroll_data = PayrollData(
                billRate=project.payroll.bill_rate,
                overtimeBillrate=project.payroll.overtime_billrate,
            )

        project_data = ProjectData(
            id=project.id,
            name=project.name,
            description=project.description,
            employees=project.employees,
            statuses=project.statuses,
            priorities=project.priorities,
            billable=project.billable,
            deadline=int(project.deadline.timestamp() * 1000) if project.deadline else None,
            payroll=payroll_data,
            archived=project.archived,
            creatorId=project.creator_id,
            organizationId=project.organization_id,
            teams=project.teams,
            createdAt=created_at_timestamp,
        )
        project_list.append(project_data)

    return project_list


@project_router.get("/{project_id}", response_model=ProjectData)
async def get_project(project_id: str) -> ProjectData:
    project_service = ProjectService()

    project = project_service.get_project_by_id(project_id)

    if not project:
        raise NotFoundError(ResponseMessages.PROJECT_NOT_FOUND)

    created_at_timestamp = int(project.created_at.timestamp() * 1000)

    payroll_data = None
    if project.payroll:
        payroll_data = PayrollData(
            billRate=project.payroll.bill_rate,
            overtimeBillrate=project.payroll.overtime_billrate,
        )

    return ProjectData(
        id=project.id,
        name=project.name,
        description=project.description,
        employees=project.employees,
        statuses=project.statuses,
        priorities=project.priorities,
        billable=project.billable,
        deadline=int(project.deadline.timestamp() * 1000) if project.deadline else None,
        payroll=payroll_data,
        archived=project.archived,
        creatorId=project.creator_id,
        organizationId=project.organization_id,
        teams=project.teams,
        createdAt=created_at_timestamp,
    )


@project_router.put("/{project_id}", response_model=ProjectData)
async def update_project(project_id: str, request_data: ProjectUpdateRequest) -> ProjectData:
    project_service = ProjectService()

    payroll_dict = None
    if request_data.payroll:
        payroll_dict = {
            "bill_rate": request_data.payroll.billRate,
            "overtime_billrate": request_data.payroll.overtimeBillrate,
        }

    deadline_datetime = None
    if request_data.deadline is not None:
        deadline_datetime = datetime.fromtimestamp(request_data.deadline / 1000)

    project = project_service.update_project(
        project_id=project_id,
        name=request_data.name,
        description=request_data.description,
        employees=request_data.employees,
        statuses=request_data.statuses,
        priorities=request_data.priorities,
        billable=request_data.billable,
        deadline=deadline_datetime,
        payroll=payroll_dict,
    )

    created_at_timestamp = int(project.created_at.timestamp() * 1000)

    payroll_data = None
    if project.payroll:
        payroll_data = PayrollData(
            billRate=project.payroll.bill_rate,
            overtimeBillrate=project.payroll.overtime_billrate,
        )

    return ProjectData(
        id=project.id,
        name=project.name,
        description=project.description,
        employees=project.employees,
        statuses=project.statuses,
        priorities=project.priorities,
        billable=project.billable,
        deadline=int(project.deadline.timestamp() * 1000) if project.deadline else None,
        payroll=payroll_data,
        archived=project.archived,
        creatorId=project.creator_id,
        organizationId=project.organization_id,
        teams=project.teams,
        createdAt=created_at_timestamp,
    )


@project_router.delete("/{project_id}")
async def delete_project(project_id: str) -> dict[str, str]:
    project_service = ProjectService()

    success = project_service.delete_project(project_id)

    if success:
        return {"message": ResponseMessages.PROJECT_DELETED}
    else:
        return {"message": ResponseMessages.PROJECT_DELETE_FAILED}
