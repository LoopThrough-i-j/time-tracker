from database.mongodb.actions.time_log import TimeLogActions
from database.mongodb.models.time_log import TimeLog


class AnalyticsService:
    def __init__(self):
        self.time_log_actions = TimeLogActions()

    def get_window_analytics(
        self,
        start_time: int | None = None,
        end_time: int | None = None,
        employee_id: str | None = None,
        project_id: str | None = None,
        task_id: str | None = None,
        team_id: str | None = None,
        shift_id: str | None = None,
        timezone: str | None = None,
    ) -> list[TimeLog]:
        time_logs = self.time_log_actions.get_analytics_logs(
            start_time=start_time,
            end_time=end_time,
            employee_id=employee_id,
            project_id=project_id,
            task_id=task_id,
            team_id=team_id,
            shift_id=shift_id,
            timezone=timezone,
        )

        return [log for log in time_logs if log.start != log.end]

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
    ) -> list[dict[str, any]]:
        time_logs = self.time_log_actions.get_project_time_logs(
            start_time=start_time,
            end_time=end_time,
            employee_id=employee_id,
            team_id=team_id,
            project_id=project_id,
            task_id=task_id,
            shift_id=shift_id,
            timezone=timezone,
        )

        project_analytics = {}

        for log in time_logs:
            if log.start == log.end:
                continue

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

        result = []
        for project_id, analytics in project_analytics.items():
            result.append(
                {
                    "id": project_id,
                    "time": analytics["time"],
                    "costs": round(analytics["costs"], 2),
                    "income": round(analytics["income"], 2),
                }
            )

        result.sort(key=lambda x: x["time"], reverse=True)
        return result
