from pydantic import Field

from app.dto.request.base import BaseRequest
from database.mongodb.models.time_log import TimeLogType


class CreateTimeLogRequest(BaseRequest):
    type: TimeLogType = Field()
    note: str | None = Field(default=None, max_length=1000)
    start: int = Field(ge=0)
    end: int = Field(ge=0)
    timezone_offset: int = Field()
    shift_id: str | None = Field(default=None, min_length=1)
    project_id: str = Field(min_length=1)
    task_id: str = Field(min_length=1)
    overtime: bool = Field(default=False)
    user: str = Field(min_length=1, max_length=100)
    computer: str | None = Field(default=None, max_length=100)
    domain: str | None = Field(default=None, max_length=100)
    hwid: str | None = Field(default=None, max_length=100)
    operating_system: str | None = Field(default=None, max_length=50)
    os_version: str | None = Field(default=None, max_length=50)
    employee_id: str = Field(min_length=1)
    negative_time: int = Field(default=0, ge=0)
