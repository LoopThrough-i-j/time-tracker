from pydantic import Field

from app.dto.response.base import BaseResponseDataModel


class TaskResponse(BaseResponseDataModel):
    id: str = Field()
    name: str | None = Field()
    description: str | None = Field()
    employees: list[str] = Field()
    project_id: str = Field(alias="projectId")
    deadline: int | None = Field()
    status: str | None = Field()
    labels: list[str] = Field()
    priority: str | None = Field()
    billable: bool = Field()
    created_at: int = Field(alias="createdAt")
    updated_at: int = Field(alias="updatedAt")


class TaskListResponse(BaseResponseDataModel):
    tasks: list[TaskResponse] = Field()
    total: int = Field()
