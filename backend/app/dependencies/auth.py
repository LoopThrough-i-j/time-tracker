from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.constants.response_messages import ResponseMessages

from constants.exceptions import BadRequestError
from services.auth import AuthService

security = HTTPBearer()


def get_current_employee_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    auth_service = AuthService()

    payload = auth_service.verify_token(credentials.credentials)
    employee_id = payload.get("employee_id")

    if not employee_id:
        raise BadRequestError(ResponseMessages.INVALID_TOKEN_EMPLOYEE_ID_NOT_FOUND)

    return employee_id
