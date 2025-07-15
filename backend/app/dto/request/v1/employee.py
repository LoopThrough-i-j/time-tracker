from pydantic import EmailStr, Field

from app.dto.request.base import BaseRequestModel


class EmployeeInviteRequest(BaseRequestModel):
    name: str = Field(description="Employee full name")
    email: EmailStr = Field(description="Employee email address")
    team_id: str = Field(alias="teamId", description="Team identifier")


class EmployeeUpdateRequest(BaseRequestModel):
    name: str | None = Field(description="Employee full name", default=None)
    email: EmailStr | None = Field(description="Employee email address", default=None)
    team_id: str | None = Field(alias="teamId", description="Team identifier", default=None)
    projects: list[str] | None = Field(description="List of project identifiers", default=None)
