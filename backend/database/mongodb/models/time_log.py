from datetime import datetime
from enum import Enum

from pydantic import Field

from database.constants.collections import DatabaseCollections
from database.mongodb.models.base import BaseMongoModel


class TimeLogType(str, Enum):
    MANUAL = "manual"
    AUTOMATIC = "automatic"


class TimeLog(BaseMongoModel):
    collection = DatabaseCollections.TIME_LOGS

    type: TimeLogType = Field()
    note: str | None = Field(default=None)
    start: datetime = Field()
    end: datetime = Field()
    timezone_offset: int = Field()
    shift_id: str | None = Field(default=None)
    project_id: str = Field()
    task_id: str = Field()
    paid: bool = Field(default=False)
    billable: bool = Field(default=True)
    overtime: bool = Field(default=False)
    bill_rate: float = Field(default=0.0)
    overtime_bill_rate: float = Field(default=0.0)
    pay_rate: float = Field(default=0.0)
    overtime_pay_rate: float = Field(default=0.0)
    task_status: str | None = Field(default=None)
    task_priority: str | None = Field(default=None)
    user: str = Field()
    computer: str | None = Field(default=None)
    domain: str | None = Field(default=None)
    name: str = Field()
    hwid: str | None = Field(default=None)
    operating_system: str | None = Field(default=None)
    os_version: str | None = Field(default=None)
    processed: bool = Field(default=False)
    employee_id: str = Field()
    team_id: str | None = Field(default=None)
    shared_settings_id: str | None = Field(default=None)
    organization_id: str | None = Field(default=None)
    start_translated: datetime = Field()
    end_translated: datetime = Field()
    negative_time: int = Field(default=0)
    deleted_screenshots: int = Field(default=0)
    index: str | None = Field(default=None, alias="_index")
