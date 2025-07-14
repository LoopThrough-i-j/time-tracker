from pydantic import Field

from app.dto.request.base import BaseRequest


class CreateTaskRequest(BaseRequest):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, min_length=1, max_length=1000)
    employees: list[str] = Field(default_factory=list)
    project_id: str = Field(min_length=1)
    deadline: int | None = Field(default=None)
    status: str | None = Field(default=None)
    labels: list[str] = Field(default_factory=list)
    priority: str | None = Field(default=None)
    billable: bool | None = Field(default=None)


class UpdateTaskRequest(BaseRequest):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, min_length=1, max_length=1000)
    employees: list[str] | None = Field(default=None)
    project_id: str | None = Field(default=None, min_length=1)
    deadline: int | None = Field(default=None)
    status: str | None = Field(default=None)
    labels: list[str] | None = Field(default=None)
    priority: str | None = Field(default=None)
    billable: bool | None = Field(default=None)
