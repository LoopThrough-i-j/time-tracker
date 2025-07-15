from pydantic import EmailStr, Field

from app.dto.request.base import BaseRequest


class EmployeeLoginRequest(BaseRequest):
    email: EmailStr = Field()
    password: str = Field(min_length=1)


class EmployeeRegisterRequest(BaseRequest):
    email: EmailStr = Field()
    password: str = Field(min_length=6, max_length=100)


class SignupLinkRequest(BaseRequest):
    employee_id: str = Field()
    expiry_hours: int = Field(default=24, ge=1, le=168)
