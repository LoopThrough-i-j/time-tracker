from pydantic import Field

from app.dto.response.base import BaseResponseDataModel

from database.mongodb.models.time_log import TimeLogType


class TimeLogResponse(BaseResponseDataModel):
    id: str = Field()
    type: TimeLogType = Field()
    note: str | None = Field()
    start: int = Field()
    end: int = Field()
    timezone_offset: int = Field(alias="timezoneOffset")
    shift_id: str | None = Field(alias="shiftId")
    project_id: str = Field(alias="projectId")
    task_id: str = Field(alias="taskId")
    paid: bool = Field()
    billable: bool = Field()
    overtime: bool = Field()
    bill_rate: float = Field(alias="billRate")
    overtime_bill_rate: float = Field(alias="overtimeBillRate")
    pay_rate: float = Field(alias="payRate")
    overtime_pay_rate: float = Field(alias="overtimePayRate")
    task_status: str | None = Field(alias="taskStatus")
    task_priority: str | None = Field(alias="taskPriority")
    user: str = Field()
    computer: str | None = Field()
    domain: str | None = Field()
    name: str = Field()
    hwid: str | None = Field()
    operating_system: str | None = Field()
    os_version: str | None = Field(alias="osVersion")
    processed: bool = Field()
    employee_id: str = Field(alias="employeeId")
    team_id: str | None = Field(alias="teamId")
    shared_settings_id: str | None = Field(alias="sharedSettingsId")
    organization_id: str | None = Field(alias="organizationId")
    start_translated: int = Field(alias="startTranslated")
    end_translated: int = Field(alias="endTranslated")
    negative_time: int = Field(alias="negativeTime")
    deleted_screenshots: int = Field(alias="deletedScreenshots")
    index: str | None = Field(alias="_index")
    created_at: int = Field(alias="createdAt")
    updated_at: int = Field(alias="updatedAt")


class TimeLogListResponse(BaseResponseDataModel):
    time_logs: list[TimeLogResponse] = Field()
    total: int = Field()
