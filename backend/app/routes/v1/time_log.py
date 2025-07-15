from datetime import datetime, timezone

from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_employee_id
from app.dto.request.v1.time_log import StartTimeLogRequest
from app.dto.response.v1.time_log import TimeLogResponse
from app.tags import APITags

from services.time_log import TimeLogService

time_log_router = APIRouter(prefix="/time-log", tags=[APITags.TIME_LOG.name])


@time_log_router.post("/start", response_model=TimeLogResponse)
def start_time_log(
    request_data: StartTimeLogRequest, employee_id: str = Depends(get_current_employee_id)
) -> TimeLogResponse:
    time_log_service = TimeLogService()

    now = datetime.now(timezone.utc)

    time_log = time_log_service.start_time_log(
        time_log_type=request_data.type,
        note=request_data.note,
        start=now,
        timezone_offset=request_data.timezone_offset,
        shift_id=request_data.shift_id,
        project_id=request_data.project_id,
        task_id=request_data.task_id,
        overtime=request_data.overtime,
        user=request_data.user,
        computer=request_data.computer,
        domain=request_data.domain,
        hwid=request_data.hwid,
        operating_system=request_data.operating_system,
        os_version=request_data.os_version,
        employee_id=employee_id,
    )

    start_translated = int(time_log.start.timestamp() * 1000 - time_log.timezone_offset)
    end_translated = int(time_log.end.timestamp() * 1000 - time_log.timezone_offset)

    return TimeLogResponse(
        id=time_log.id,
        type=time_log.type,
        note=time_log.note,
        start=int(time_log.start.timestamp() * 1000),
        end=int(time_log.end.timestamp() * 1000),
        timezone_offset=time_log.timezone_offset,
        shift_id=time_log.shift_id,
        project_id=time_log.project_id,
        task_id=time_log.task_id,
        paid=time_log.paid,
        billable=time_log.billable,
        overtime=time_log.overtime,
        bill_rate=time_log.bill_rate,
        overtime_bill_rate=time_log.overtime_bill_rate,
        pay_rate=time_log.pay_rate,
        overtime_pay_rate=time_log.overtime_pay_rate,
        task_status=time_log.task_status,
        task_priority=time_log.task_priority,
        user=time_log.user,
        computer=time_log.computer,
        domain=time_log.domain,
        name=time_log.name,
        hwid=time_log.hwid,
        operating_system=time_log.operating_system,
        os_version=time_log.os_version,
        processed=time_log.processed,
        employee_id=time_log.employee_id,
        team_id=time_log.team_id,
        shared_settings_id=time_log.shared_settings_id,
        organization_id=time_log.organization_id,
        start_translated=start_translated,
        end_translated=end_translated,
        negative_time=time_log.negative_time,
        deleted_screenshots=time_log.deleted_screenshots,
        index=time_log.index,
        created_at=int(time_log.created_at.timestamp() * 1000),
        updated_at=int(time_log.updated_at.timestamp() * 1000),
    )


@time_log_router.put("/{time_log_id}/update", response_model=TimeLogResponse)
def update_time_log(time_log_id: str, employee_id: str = Depends(get_current_employee_id)) -> TimeLogResponse:
    time_log_service = TimeLogService()

    now = datetime.now(timezone.utc)

    time_log = time_log_service.update_time_log(
        time_log_id=time_log_id,
        employee_id=employee_id,
        end=now,
    )

    start_translated = int(time_log.start.timestamp() * 1000 - time_log.timezone_offset)
    end_translated = int(time_log.end.timestamp() * 1000 - time_log.timezone_offset)

    return TimeLogResponse(
        id=time_log.id,
        type=time_log.type,
        note=time_log.note,
        start=int(time_log.start.timestamp() * 1000),
        end=int(time_log.end.timestamp() * 1000),
        timezone_offset=time_log.timezone_offset,
        shift_id=time_log.shift_id,
        project_id=time_log.project_id,
        task_id=time_log.task_id,
        paid=time_log.paid,
        billable=time_log.billable,
        overtime=time_log.overtime,
        bill_rate=time_log.bill_rate,
        overtime_bill_rate=time_log.overtime_bill_rate,
        pay_rate=time_log.pay_rate,
        overtime_pay_rate=time_log.overtime_pay_rate,
        task_status=time_log.task_status,
        task_priority=time_log.task_priority,
        user=time_log.user,
        computer=time_log.computer,
        domain=time_log.domain,
        name=time_log.name,
        hwid=time_log.hwid,
        operating_system=time_log.operating_system,
        os_version=time_log.os_version,
        processed=time_log.processed,
        employee_id=time_log.employee_id,
        team_id=time_log.team_id,
        shared_settings_id=time_log.shared_settings_id,
        organization_id=time_log.organization_id,
        start_translated=start_translated,
        end_translated=end_translated,
        negative_time=time_log.negative_time,
        deleted_screenshots=time_log.deleted_screenshots,
        index=time_log.index,
        created_at=int(time_log.created_at.timestamp() * 1000),
        updated_at=int(time_log.updated_at.timestamp() * 1000),
    )
