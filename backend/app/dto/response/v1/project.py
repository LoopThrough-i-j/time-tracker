from pydantic import Field

from app.dto.response.base import BaseResponseDataModel


class PayrollData(BaseResponseDataModel):
    bill_rate: float = Field(alias="billRate", description="Bill rate")
    overtime_billrate: float = Field(alias="overtimeBillrate", description="Overtime bill rate")


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
    creator_id: str = Field(alias="creatorId", description="Creator user ID")
    organization_id: str = Field(alias="organizationId", description="Organization ID")
    teams: list[str] = Field(description="List of team IDs")
    created_at: int = Field(alias="createdAt", description="Creation timestamp in milliseconds")
