from pydantic import EmailStr, Field

from app.dto.request.base import BaseRequest


class EmployeeLoginRequest(BaseRequest):
    email: EmailStr = Field()
    password: str = Field(min_length=1)


class EmployeeRegisterRequest(BaseRequest):
    email: EmailStr = Field()
    password: str = Field(min_length=6, max_length=100)
