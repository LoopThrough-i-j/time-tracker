from fastapi import APIRouter, Query

from app.dto.response.v1.analytics import ProjectTimeAnalytics
from app.dto.response.v1.time_log import TimeLogResponse
from app.tags import APITags

from services.analytics import AnalyticsService

analytics_router = APIRouter(prefix="/analytics", tags=[APITags.TIME_LOG.name])


@analytics_router.get("/window", response_model=list[TimeLogResponse])
def get_analytics_window(
    start: int = Query(),
    end: int = Query(),
    timezone: str | None = Query(default=None),
    employeeId: str | None = Query(default=None),
    teamId: str | None = Query(default=None),
    projectId: str | None = Query(default=None),
    taskId: str | None = Query(default=None),
    shiftId: str | None = Query(default=None),
) -> list[TimeLogResponse]:
    analytics_service = AnalyticsService()

    time_logs = analytics_service.get_window_analytics(
        start_time=start,
        end_time=end,
        employee_id=employeeId,
        project_id=projectId,
        task_id=taskId,
        team_id=teamId,
        shift_id=shiftId,
        timezone=timezone,
    )

    return [
        TimeLogResponse(
            id=str(log.id),
            type=log.type,
            note=log.note,
            start=log.start,
            end=log.end,
            timezone_offset=log.timezone_offset,
            shift_id=log.shift_id,
            project_id=log.project_id,
            task_id=log.task_id,
            paid=log.paid,
            billable=log.billable,
            overtime=log.overtime,
            bill_rate=log.bill_rate,
            overtime_bill_rate=log.overtime_bill_rate,
            pay_rate=log.pay_rate,
            overtime_pay_rate=log.overtime_pay_rate,
            task_status=log.task_status,
            task_priority=log.task_priority,
            user=log.user,
            computer=log.computer,
            domain=log.domain,
            name=log.name,
            hwid=log.hwid,
            os=log.os,
            os_version=log.os_version,
            processed=log.processed,
            employee_id=log.employee_id,
            team_id=log.team_id,
            shared_settings_id=log.shared_settings_id,
            organization_id=log.organization_id,
            start_translated=log.start_translated,
            end_translated=log.end_translated,
            negative_time=log.negative_time,
            deleted_screenshots=log.deleted_screenshots,
            index=log.index,
            created_at=int(log.created_at.timestamp() * 1000),
            updated_at=int(log.updated_at.timestamp() * 1000),
        )
        for log in time_logs
    ]


@analytics_router.get("/project-time", response_model=list[ProjectTimeAnalytics])
def get_project_time_analytics(
    start: int = Query(),
    end: int = Query(),
    timezone: str | None = Query(default=None),
    employeeId: str | None = Query(default=None),
    teamId: str | None = Query(default=None),
    projectId: str | None = Query(default=None),
    taskId: str | None = Query(default=None),
    shiftId: str | None = Query(default=None),
) -> list[ProjectTimeAnalytics]:
    analytics_service = AnalyticsService()

    project_analytics = analytics_service.get_project_time_analytics(
        start_time=start,
        end_time=end,
        employee_id=employeeId,
        team_id=teamId,
        project_id=projectId,
        task_id=taskId,
        shift_id=shiftId,
        timezone=timezone,
    )

    return [
        ProjectTimeAnalytics(
            id=project["id"],
            time=project["time"],
            costs=project["costs"],
            income=project["income"],
        )
        for project in project_analytics
    ]
