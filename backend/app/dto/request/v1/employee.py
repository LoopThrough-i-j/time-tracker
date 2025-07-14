from pydantic import EmailStr, Field

from app.dto.request.base import BaseRequestModel


class EmployeeInviteRequest(BaseRequestModel):
    name: str = Field(description="Employee full name")
    email: EmailStr = Field(description="Employee email address")
    teamId: str = Field(description="Team identifier")


class EmployeeUpdateRequest(BaseRequestModel):
    name: str = Field(description="Employee full name")
    email: EmailStr = Field(description="Employee email address")
    teamId: str = Field(description="Team identifier")
    projects: list[str] = Field(description="List of project identifiers", default_factory=list)
