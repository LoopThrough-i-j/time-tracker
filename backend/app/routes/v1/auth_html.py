from fastapi import APIRouter, Form, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from constants.exceptions import BadRequestError, NotFoundError
from services.auth import AuthService

templates = Jinja2Templates(directory="app/templates")
auth_html_router = APIRouter(prefix="/auth", tags=["Auth HTML"])


@auth_html_router.get("/signup", response_class=HTMLResponse)
def signup_form(request: Request, token: str = Query(...), error: str = None, success: str = None):
    auth_service = AuthService()
    payload = auth_service.decrypt_signup_token(token)
    employee_id = payload["employee_id"]

    employee = auth_service.get_employee_by_id(employee_id)

    if not employee:
        raise NotFoundError("Employee not found")

    if employee.password:
        raise BadRequestError("Employee has already signed up")

    return templates.TemplateResponse(
        "signup.html",
        {"request": request, "error": error, "success": success, "token": token, "employee_email": employee.email},
    )


@auth_html_router.post("/signup", response_class=HTMLResponse)
def process_signup_form(request: Request, token: str = Form(...), email: str = Form(...), password: str = Form(...)):
    try:
        auth_service = AuthService()
        payload = auth_service.decrypt_signup_token(token)
        employee_id = payload["employee_id"]

        employee = auth_service.update_employee_password(email=email, password=password)

        if employee.id != employee_id:
            error_employee = auth_service.get_employee_by_id(employee_id)
            return templates.TemplateResponse(
                "signup.html",
                {
                    "request": request,
                    "error": "Invalid signup link for this email address",
                    "token": token,
                    "employee_email": error_employee.email if error_employee else "",
                },
            )

        return templates.TemplateResponse("success.html", {"request": request, "employee": employee})

    except ValueError:
        return templates.TemplateResponse(
            "signup.html",
            {"request": request, "error": "Invalid signup link", "token": token, "employee_email": ""},
        )
    except (BadRequestError, NotFoundError) as e:
        return templates.TemplateResponse(
            "signup.html", {"request": request, "error": str(e), "token": token, "employee_email": ""}
        )
    except Exception:
        return templates.TemplateResponse(
            "signup.html",
            {
                "request": request,
                "error": "An unexpected error occurred. Please try again.",
                "token": token,
                "employee_email": "",
            },
        )
