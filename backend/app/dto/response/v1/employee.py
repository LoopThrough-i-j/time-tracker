from pydantic import Field

from app.dto.response.base import BaseResponseDataModel


class EmployeeData(BaseResponseDataModel):
    id: str = Field(description="Employee unique identifier")
    name: str = Field(description="Employee full name")
    email: str = Field(description="Employee email address")
    teamId: str = Field(description="Team identifier")
    identifier: str = Field(description="Employee identifier")
    type: str = Field(description="Employee type (personal/office)")
    projects: list[str] = Field(description="List of project identifiers")
    deactivated: int = Field(description="Deactivation status (0=active, 1=deactivated)")
    invited: int = Field(description="Invitation timestamp in milliseconds")
    createdAt: int = Field(description="Creation timestamp in milliseconds")
