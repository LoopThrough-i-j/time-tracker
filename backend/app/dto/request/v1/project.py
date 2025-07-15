from pydantic import Field

from app.dto.request.base import BaseRequestModel


class PayrollRequest(BaseRequestModel):
    bill_rate: float = Field(alias="billRate", description="Bill rate")
    overtime_billrate: float = Field(alias="overtimeBillrate", description="Overtime bill rate")


class ProjectCreateRequest(BaseRequestModel):
    name: str = Field(description="Project name")
    description: str = Field(description="Project description")
    employees: list[str] = Field(description="List of employee IDs", default_factory=list)
    statuses: list[str] = Field(description="List of project statuses", default_factory=list)
    priorities: list[str] = Field(description="List of project priorities", default_factory=list)
    billable: bool = Field(description="Whether project is billable", default=False)
    deadline: int | None = Field(description="Project deadline in milliseconds", default=None)
    payroll: PayrollRequest | None = Field(description="Payroll information", default=None)


class ProjectUpdateRequest(BaseRequestModel):
    name: str | None = Field(description="Project name", default=None)
    description: str | None = Field(description="Project description", default=None)
    employees: list[str] | None = Field(description="List of employee IDs", default=None)
    statuses: list[str] | None = Field(description="List of project statuses", default=None)
    priorities: list[str] | None = Field(description="List of project priorities", default=None)
    billable: bool | None = Field(description="Whether project is billable", default=None)
    deadline: int | None = Field(description="Project deadline in milliseconds", default=None)
    payroll: PayrollRequest | None = Field(description="Payroll information", default=None)
