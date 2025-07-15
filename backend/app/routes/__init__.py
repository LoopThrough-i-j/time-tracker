from fastapi import APIRouter

from app.routes.v1.analytics import analytics_router
from app.routes.v1.auth import auth_router
from app.routes.v1.employee import employee_router
from app.routes.v1.project import project_router
from app.routes.v1.task import task_router
from app.routes.v1.time_log import time_log_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(auth_router)
v1_router.include_router(employee_router)
v1_router.include_router(project_router)
v1_router.include_router(task_router)
v1_router.include_router(time_log_router)
v1_router.include_router(analytics_router)
