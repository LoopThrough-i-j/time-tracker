from fastapi import APIRouter

from app.dto.request.v1.auth import EmployeeLoginRequest, SignupLinkRequest
from app.dto.response.v1.auth import EmployeeAuthResponse, SignupLinkResponse
from app.tags import APITags

from services.auth import AuthService

auth_router = APIRouter(prefix="/auth", tags=[APITags.EMPLOYEE.name])


@auth_router.post("/get-signup-link", response_model=SignupLinkResponse)
def get_signup_link(request_data: SignupLinkRequest) -> SignupLinkResponse:
    auth_service = AuthService()

    employee = auth_service.get_employee_by_id(request_data.employee_id)
    if not employee:
        from constants.exceptions import NotFoundError

        raise NotFoundError("Employee not found")

    token = auth_service.generate_signup_token(request_data.employee_id, request_data.expiry_hours)
    signup_link = f"/auth/signup?token={token}"

    return SignupLinkResponse(signup_link=signup_link, expiry_hours=request_data.expiry_hours)


@auth_router.post("/login", response_model=EmployeeAuthResponse)
def login_employee(request_data: EmployeeLoginRequest) -> EmployeeAuthResponse:
    auth_service = AuthService()

    employee, access_token = auth_service.authenticate_employee(
        email=request_data.email, password=request_data.password
    )

    return EmployeeAuthResponse(
        access_token=access_token,
        employee_id=employee.id,
        name=employee.name,
        email=employee.email,
        team_id=employee.team_id,
    )
