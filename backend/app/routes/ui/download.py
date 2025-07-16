from fastapi import APIRouter
from fastapi.responses import FileResponse
import os

from constants.exceptions import NotFoundError

download_html_router = APIRouter(prefix="/download", tags=["Download"])


@download_html_router.get("/app/mac")
def download_mac_app():
    file_path = "app/templates/Mercor Time Tracker-1.0.0-arm64.dmg"

    if os.path.exists(file_path):
        return FileResponse(
            path=file_path,
            filename="MercorTimeTracker-Mac.dmg",
            media_type="application/octet-stream",
        )
    else:
        raise NotFoundError("Mac application not found")
