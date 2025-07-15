from datetime import datetime

from database.mongodb.actions.base import BaseActions
from database.mongodb.models.time_log import TimeLog, TimeLogType


class TimeLogActions(BaseActions[TimeLog]):
    def __init__(self) -> None:
        super().__init__(TimeLog)

    def create_time_log(
        self,
        type: TimeLogType,
        start: int,
        end: int,
        timezone_offset: int,
        project_id: str,
        task_id: str,
        user: str,
        name: str,
        employee_id: str,
        start_translated: int,
        end_translated: int,
        note: str | None = None,
        shift_id: str | None = None,
        paid: bool = False,
        billable: bool = True,
        overtime: bool = False,
        bill_rate: float = 0.0,
        overtime_bill_rate: float = 0.0,
        pay_rate: float = 0.0,
        overtime_pay_rate: float = 0.0,
        task_status: str | None = None,
        task_priority: str | None = None,
        computer: str | None = None,
        domain: str | None = None,
        hwid: str | None = None,
        operating_system: str | None = None,
        os_version: str | None = None,
        processed: bool = False,
        team_id: str | None = None,
        shared_settings_id: str | None = None,
        negative_time: int = 0,
        deleted_screenshots: int = 0,
        index: str | None = None,
    ) -> TimeLog:

        time_log = TimeLog(
            type=type,
            note=note,
            start=datetime.fromtimestamp(start / 1000),
            end=datetime.fromtimestamp(end / 1000),
            timezone_offset=timezone_offset,
            shift_id=shift_id,
            project_id=project_id,
            task_id=task_id,
            paid=paid,
            billable=billable,
            overtime=overtime,
            bill_rate=bill_rate,
            overtime_bill_rate=overtime_bill_rate,
            pay_rate=pay_rate,
            overtime_pay_rate=overtime_pay_rate,
            task_status=task_status,
            task_priority=task_priority,
            user=user,
            computer=computer,
            domain=domain,
            name=name,
            hwid=hwid,
            operating_system=operating_system,
            os_version=os_version,
            processed=processed,
            employee_id=employee_id,
            team_id=team_id,
            shared_settings_id=shared_settings_id,
            start_translated=datetime.fromtimestamp(start_translated / 1000),
            end_translated=datetime.fromtimestamp(end_translated / 1000),
            negative_time=negative_time,
            deleted_screenshots=deleted_screenshots,
            index=index,
        )
        return self.insert_record(time_log)

    def get_analytics_logs(
        self,
        start_time: int | None = None,
        end_time: int | None = None,
        employee_id: str | None = None,
        project_id: str | None = None,
        task_id: str | None = None,
        team_id: str | None = None,
        shift_id: str | None = None,
        timezone: str | None = None,
        billable: bool | None = None,
        processed: bool | None = None,
        limit: int | None = None,
        offset: int | None = None,
    ) -> list[TimeLog]:
        query = {}

        if start_time is not None and end_time is not None:
            query["start"] = {
                "$gte": datetime.fromtimestamp(start_time / 1000),
                "$lte": datetime.fromtimestamp(end_time / 1000),
            }
        elif start_time is not None:
            query["start"] = {"$gte": datetime.fromtimestamp(start_time / 1000)}
        elif end_time is not None:
            query["end"] = {"$lte": datetime.fromtimestamp(end_time / 1000)}

        if employee_id is not None:
            query["employee_id"] = employee_id

        if project_id is not None:
            query["project_id"] = project_id

        if task_id is not None:
            query["task_id"] = task_id

        if team_id is not None:
            query["team_id"] = team_id

        if shift_id is not None:
            query["shift_id"] = shift_id

        if billable is not None:
            query["billable"] = billable

        if processed is not None:
            query["processed"] = processed

        sort = [("start", -1)]

        return self.find_records(
            query=query,
            sort=sort,
            offset=offset,
            limit=limit,
            is_active=True,
            is_deleted=False,
        )

    def get_project_time_analytics(
        self,
        start_time: int,
        end_time: int,
        employee_id: str | None = None,
        team_id: str | None = None,
        project_id: str | None = None,
        task_id: str | None = None,
        shift_id: str | None = None,
        timezone: str | None = None,
    ) -> dict[str, dict[str, float]]:
        query = {
            "start": {
                "$gte": datetime.fromtimestamp(start_time / 1000),
                "$lte": datetime.fromtimestamp(end_time / 1000),
            }
        }

        if employee_id is not None:
            query["employee_id"] = employee_id

        if team_id is not None:
            query["team_id"] = team_id

        if project_id is not None:
            query["project_id"] = project_id

        if task_id is not None:
            query["task_id"] = task_id

        if shift_id is not None:
            query["shift_id"] = shift_id

        time_logs = self.find_records(
            query=query,
            sort=[("start", -1)],
            is_active=True,
            is_deleted=False,
        )

        project_analytics = {}

        for log in time_logs:
            project_id = log.project_id

            if project_id not in project_analytics:
                project_analytics[project_id] = {"time": 0, "costs": 0.0, "income": 0.0}

            duration_ms = int((log.end - log.start).total_seconds() * 1000)

            duration_hours = duration_ms / 1000 / 3600

            project_analytics[project_id]["time"] += duration_ms

            costs = duration_hours * log.pay_rate
            project_analytics[project_id]["costs"] += costs

            income = duration_hours * log.bill_rate
            project_analytics[project_id]["income"] += income

        return project_analytics
