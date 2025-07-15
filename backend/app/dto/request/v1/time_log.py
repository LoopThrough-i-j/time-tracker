from pydantic import Field

from app.dto.request.base import BaseRequestModel

from database.mongodb.models.time_log import TimeLogType


class StartTimeLogRequest(BaseRequestModel):
    type: TimeLogType = Field()
    note: str | None = Field(default=None, max_length=1000)
    timezone_offset: int = Field(alias="timezoneOffset")
    shift_id: str | None = Field(default=None, min_length=1, alias="shiftId")
    project_id: str = Field(min_length=1, alias="projectId")
    task_id: str = Field(min_length=1, alias="taskId")
    overtime: bool = Field(default=False)
    user: str = Field(min_length=1, max_length=100)
    computer: str | None = Field(default=None, max_length=100)
    domain: str | None = Field(default=None, max_length=100)
    hwid: str | None = Field(default=None, max_length=100)
    operating_system: str | None = Field(default=None, max_length=50, alias="operatingSystem")
    os_version: str | None = Field(default=None, max_length=50, alias="osVersion")
