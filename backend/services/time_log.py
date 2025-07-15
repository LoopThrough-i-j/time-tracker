from datetime import datetime

from app.constants.response_messages import ResponseMessages

from constants.exceptions import BadRequestError, NotFoundError
from database.mongodb.actions.employee import EmployeeActions
from database.mongodb.actions.project import ProjectActions
from database.mongodb.actions.task import TaskActions
from database.mongodb.actions.time_log import TimeLogActions
from database.mongodb.models.time_log import TimeLog, TimeLogType


class TimeLogService:
    def __init__(self):
        self.time_log_actions = TimeLogActions()
        self.task_actions = TaskActions()
        self.project_actions = ProjectActions()
        self.employee_actions = EmployeeActions()

    def start_time_log(
        self,
        time_log_type: TimeLogType,
        start: datetime,
        timezone_offset: int,
        project_id: str,
        task_id: str,
        user: str,
        employee_id: str,
        note: str | None = None,
        shift_id: str | None = None,
        overtime: bool = False,
        computer: str | None = None,
        domain: str | None = None,
        hwid: str | None = None,
        operating_system: str | None = None,
        os_version: str | None = None,
    ) -> TimeLog:

        task = self.task_actions.get_by_id(task_id)
        if not task:
            raise NotFoundError(f"Task with id {task_id} not found")

        billable = task.billable
        task_status = task.status
        task_priority = task.priority

        project = self.project_actions.get_by_id(project_id)
        if not project:
            raise NotFoundError(f"Project with id {project_id} not found")

        if project.payroll:
            bill_rate = project.payroll.bill_rate
            overtime_bill_rate = project.payroll.overtime_billrate
        else:
            bill_rate = 0.0
            overtime_bill_rate = 0.0

        employee = self.employee_actions.get_by_id(employee_id)
        if not employee:
            raise NotFoundError(f"Employee with id {employee_id} not found")

        name = employee.name
        team_id = employee.team_id

        created_time_log = self.time_log_actions.create_time_log(
            type=time_log_type,
            note=note,
            start=start,
            end=start,
            timezone_offset=timezone_offset,
            shift_id=shift_id,
            project_id=project_id,
            task_id=task_id,
            paid=False,
            billable=billable,
            overtime=overtime,
            bill_rate=bill_rate,
            overtime_bill_rate=overtime_bill_rate,
            pay_rate=0.0,
            overtime_pay_rate=0.0,
            task_status=task_status,
            task_priority=task_priority,
            user=user,
            computer=computer,
            domain=domain,
            name=name,
            hwid=hwid,
            operating_system=operating_system,
            os_version=os_version,
            processed=False,
            employee_id=employee_id,
            team_id=team_id,
            shared_settings_id=None,
            negative_time=0,
            deleted_screenshots=0,
            index=None,
        )

        return created_time_log

    def update_time_log(
        self,
        time_log_id: str,
        employee_id: str,
        end: datetime,
    ) -> TimeLog:
        time_log = self.time_log_actions.get_by_id(time_log_id)
        if not time_log:
            raise NotFoundError(f"Time log with id {time_log_id} not found")

        if time_log.employee_id != employee_id:
            raise NotFoundError("Time log not found")

        more_recent_log = self.time_log_actions.find_records(
            query={"employee_id": employee_id, "start": {"$gt": time_log.start}},
            limit=1,
            is_active=True,
            is_deleted=False,
        )

        if more_recent_log:
            raise BadRequestError(ResponseMessages.TIME_LOG_UPDATE_BLOCKED)

        update_data = {
            "end": end,
        }

        updated_time_log = self.time_log_actions.update_fields(time_log_id, update_data)
        return updated_time_log
