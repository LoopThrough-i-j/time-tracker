from pydantic import Field

from app.dto.response.base import BaseResponseDataModel


class EmployeeAuthResponse(BaseResponseDataModel):
    access_token: str = Field()
    token_type: str = Field(default="bearer")
    employee_id: str = Field()
    name: str = Field()
    email: str = Field()
    team_id: str = Field()


class SignupLinkResponse(BaseResponseDataModel):
    signup_link: str = Field()
    expiry_hours: int = Field()
