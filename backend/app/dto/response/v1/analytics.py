from pydantic import Field

from app.dto.response.base import BaseResponse
from app.dto.response.v1.time_log import TimeLogResponse


class AnalyticsWindowResponse(BaseResponse):
    data: list[TimeLogResponse] = Field()
    total_records: int = Field(alias="totalRecords")
    total_duration: int = Field(alias="totalDuration")
    billable_duration: int = Field(alias="billableDuration")
    total_earnings: float = Field(alias="totalEarnings")
    billable_earnings: float = Field(alias="billableEarnings")


class ProjectTimeAnalytics(BaseResponse):
    id: str = Field()
    time: int = Field()
    costs: float = Field()
    income: float = Field()


class ProjectTimeAnalyticsResponse(BaseResponse):
    data: list[ProjectTimeAnalytics] = Field()
