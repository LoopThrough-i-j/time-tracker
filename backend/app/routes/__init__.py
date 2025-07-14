from fastapi import APIRouter

from app.routes.v1.employee import employee_router
from app.routes.v1.project import project_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(employee_router)
v1_router.include_router(project_router)
