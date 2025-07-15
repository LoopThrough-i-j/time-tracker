from datetime import datetime, timezone

from database.mongodb.actions.base import BaseActions
from database.mongodb.models.employee import Employee, EmployeeType


class EmployeeActions(BaseActions[Employee]):
    def __init__(self) -> None:
        super().__init__(Employee)

    def create_employee(
        self,
        name: str,
        email: str,
        team_id: str,
        identifier: str,
        invited_at: datetime | None = None,
        employee_type: EmployeeType = EmployeeType.PERSONAL,
    ) -> Employee:
        if invited_at is None:
            invited_at = datetime.now(timezone.utc)

        employee = Employee(
            name=name,
            email=email,
            password=None,
            team_id=team_id,
            identifier=identifier,
            type=employee_type,
            invited_at=invited_at,
        )
        return self.insert_record(employee)

    def get_by_email(self, email: str) -> Employee | None:
        employees = self.find_records(query={"email": email}, limit=1)
        return employees[0] if employees else None

    def get_by_team_id(self, team_id: str) -> list[Employee]:
        return self.find_records(query={"team_id": team_id})
