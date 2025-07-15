from pydantic import Field

from app.dto.response.base import BaseResponseDataModel


class EmployeeData(BaseResponseDataModel):
    id: str = Field(description="Employee unique identifier")
    name: str = Field(description="Employee full name")
    email: str = Field(description="Employee email address")
    team_id: str = Field(alias="teamId", description="Team identifier")
    identifier: str = Field(description="Employee identifier")
    type: str = Field(description="Employee type (personal/office)")
    projects: list[str] = Field(description="List of project identifiers")
    deactivated: int = Field(description="Deactivation status (0=active, 1=deactivated)")
    invited: int = Field(description="Invitation timestamp in milliseconds")
    created_at: int = Field(alias="createdAt", description="Creation timestamp in milliseconds")
