from fastapi import APIRouter, Form, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.constants.response_messages import ResponseMessages

from constants.exceptions import BadRequestError, NotFoundError
from services.auth import AuthService

templates = Jinja2Templates(directory="app/templates")
auth_html_router = APIRouter(prefix="/auth", tags=["Auth HTML"])


@auth_html_router.get("/signup", response_class=HTMLResponse)
def signup_form(request: Request, token: str = Query(...), error: str = None):
    try:
        auth_service = AuthService()
        payload = auth_service.decrypt_signup_token(token)
        employee_id = payload["employee_id"]

        employee = auth_service.get_employee_by_id(employee_id)

        if not employee:
            return templates.TemplateResponse(
                "signup.html",
                {
                    "request": request,
                    "error": ResponseMessages.EMPLOYEE_NOT_FOUND,
                    "token": token,
                    "employee_email": employee.email,
                },
            )

        if employee.password:
            return templates.TemplateResponse(
                "signup.html",
                {
                    "request": request,
                    "error": ResponseMessages.EMPLOYEE_ALREADY_SIGNED_UP,
                    "token": token,
                    "employee_email": employee.email,
                },
            )

        return templates.TemplateResponse(
            "signup.html",
            {"request": request, "error": error, "token": token, "employee_email": employee.email},
        )
    except ValueError:
        return templates.TemplateResponse(
            "signup.html",
            {"request": request, "error": ResponseMessages.INVALID_SIGNUP_LINK, "token": token, "employee_email": ""},
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
                "error": ResponseMessages.UNEXPECTED_ERROR,
                "token": token,
                "employee_email": "",
            },
        )


@auth_html_router.post("/signup", response_class=HTMLResponse)
def process_signup_form(request: Request, token: str = Form(...), email: str = Form(...), password: str = Form(...)):
    try:
        auth_service = AuthService()
        payload = auth_service.decrypt_signup_token(token)
        employee_id = payload["employee_id"]

        employee = auth_service.get_employee_by_id(employee_id)

        if employee.password:
            return templates.TemplateResponse(
                "signup.html",
                {
                    "request": request,
                    "error": ResponseMessages.EMPLOYEE_ALREADY_SIGNED_UP,
                    "token": token,
                    "employee_email": employee.email,
                },
            )

        employee = auth_service.update_employee_password(employee_id=employee_id, password=password)

        return templates.TemplateResponse("success.html", {"request": request, "employee": employee})

    except ValueError as e:
        print(f"Error processing signup form: {e}")
        return templates.TemplateResponse(
            "signup.html",
            {"request": request, "error": ResponseMessages.INVALID_SIGNUP_LINK, "token": token, "employee_email": ""},
        )
    except (BadRequestError, NotFoundError) as e:
        print(f"Error processing signup form: {e}")
        return templates.TemplateResponse(
            "signup.html", {"request": request, "error": str(e), "token": token, "employee_email": ""}
        )
    except Exception as e:
        print(f"Error processing signup form: {e}")
        return templates.TemplateResponse(
            "signup.html",
            {
                "request": request,
                "error": ResponseMessages.UNEXPECTED_ERROR,
                "token": token,
                "employee_email": "",
            },
        )
