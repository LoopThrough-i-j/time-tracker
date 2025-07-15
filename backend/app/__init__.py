import logging
from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.dto.response.error_response import ErrorResponse
from app.routes import html_router, v1_router
from app.tags import APITags

from constants.exceptions import BadRequestError, Error, NotFoundError
from environment import EnvironmentVariables


def create_app():
    app = FastAPI(
        title="Mercor Backend",
        debug=EnvironmentVariables.DEBUG,
        docs_url=EnvironmentVariables.DOC_URL,
        redoc_url=None,
        openapi_tags=APITags.to_list(),
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.exception_handler(BadRequestError)
    async def bad_request_exception_handler(request: Request, err: BadRequestError):
        logger = logging.getLogger()
        logger.error(f"Bad Request Error: {str(err)}", exc_info=True)

        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content=ErrorResponse(
                message=f"Failed to execute: {str(err)}",
                status=HTTPStatus.BAD_REQUEST,
            ).to_dict(),
        )

    @app.exception_handler(NotFoundError)
    async def not_found_exception_handler(request: Request, err: NotFoundError):
        logger = logging.getLogger()
        logger.error(f"Not Found Error: {str(err)}", exc_info=True)

        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content=ErrorResponse(
                message=f"Failed to execute: {str(err)}",
                status=HTTPStatus.NOT_FOUND,
            ).to_dict(),
        )

    @app.exception_handler(Error)
    async def base_error_exception_handler(request: Request, err: Error):
        logger = logging.getLogger()
        logger.error(f"Error occurred: {str(err)}", exc_info=True)

        return JSONResponse(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            content=ErrorResponse(
                message=f"Failed to execute: {str(err)}",
                status=HTTPStatus.UNPROCESSABLE_ENTITY,
            ).to_dict(),
        )

    @app.exception_handler(Exception)
    async def base_exception_handler(request: Request, err: Exception):
        logger = logging.getLogger()
        logger.error(f"Unexpected error occurred: {str(err)}", exc_info=True)

        return JSONResponse(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            content=ErrorResponse(
                message="Some error occurred from our end.",
                status=HTTPStatus.INTERNAL_SERVER_ERROR,
            ).to_dict(),
        )

    app.include_router(v1_router)
    app.include_router(html_router)

    @app.get("/")
    async def root():
        return {"message": "Mercor Backend API"}

    @app.get("/health")
    async def health_check():
        return {"status": "healthy", "service": "mercor-backend"}

    return app
