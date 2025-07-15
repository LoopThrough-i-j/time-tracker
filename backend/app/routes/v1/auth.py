from fastapi import APIRouter, Query

from app.dto.request.v1.auth import EmployeeLoginRequest, EmployeeRegisterRequest
from app.dto.response.v1.auth import EmployeeAuthResponse
from app.tags import APITags

from services.auth import AuthService

auth_router = APIRouter(prefix="/auth", tags=[APITags.EMPLOYEE.name])


@auth_router.post("/update-password", response_model=EmployeeAuthResponse)
def update_employee_password(request_data: EmployeeRegisterRequest) -> EmployeeAuthResponse:
    auth_service = AuthService()
    
    employee = auth_service.update_employee_password(
        email=request_data.email,
        password=request_data.password
    )
    
    _, access_token = auth_service.authenticate_employee(
        email=request_data.email,
        password=request_data.password
    )
    
    return EmployeeAuthResponse(
        access_token=access_token,
        employee_id=employee.id,
        name=employee.name,
        email=employee.email,
        team_id=employee.team_id
    )


@auth_router.post("/login", response_model=EmployeeAuthResponse)
def login_employee(request_data: EmployeeLoginRequest) -> EmployeeAuthResponse:
    auth_service = AuthService()
    
    employee, access_token = auth_service.authenticate_employee(
        email=request_data.email,
        password=request_data.password
    )
    
    return EmployeeAuthResponse(
        access_token=access_token,
        employee_id=employee.id,
        name=employee.name,
        email=employee.email,
        team_id=employee.team_id
    )
