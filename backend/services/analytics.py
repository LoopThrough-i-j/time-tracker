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
        return self.time_log_actions.get_analytics_logs(
            start_time=start_time,
            end_time=end_time,
            employee_id=employee_id,
            project_id=project_id,
            task_id=task_id,
            team_id=team_id,
            shift_id=shift_id,
            timezone=timezone,
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
    ) -> list[dict[str, any]]:
        project_data = self.time_log_actions.get_project_time_analytics(
            start_time=start_time,
            end_time=end_time,
            employee_id=employee_id,
            team_id=team_id,
            project_id=project_id,
            task_id=task_id,
            shift_id=shift_id,
            timezone=timezone,
        )

        result = []
        for project_id, analytics in project_data.items():
            result.append({
                "id": project_id,
                "time": analytics["time"],
                "costs": analytics["costs"],
                "income": analytics["income"],
            })

        result.sort(key=lambda x: x["time"], reverse=True)

        return result
