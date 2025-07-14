from pydantic import Field

from app.dto.response.base import BaseResponseDataModel


class PayrollData(BaseResponseDataModel):
    billRate: float = Field(description="Bill rate")
    overtimeBillrate: float = Field(description="Overtime bill rate")


class ProjectData(BaseResponseDataModel):
    id: str = Field(description="Project unique identifier")
    name: str = Field(description="Project name")
    description: str = Field(description="Project description")
    employees: list[str] = Field(description="List of employee IDs")
    statuses: list[str] = Field(description="List of project statuses")
    priorities: list[str] = Field(description="List of project priorities")
    billable: bool = Field(description="Whether project is billable")
    deadline: int | None = Field(description="Project deadline in milliseconds")
    payroll: PayrollData | None = Field(description="Payroll information")
    archived: bool = Field(description="Whether project is archived")
    creatorId: str = Field(description="Creator user ID")
    organizationId: str = Field(description="Organization ID")
    teams: list[str] = Field(description="List of team IDs")
    createdAt: int = Field(description="Creation timestamp in milliseconds")
