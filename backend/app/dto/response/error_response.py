from http import HTTPStatus

from app.dto.response.base import BaseResponseDataModel


class ErrorResponse(BaseResponseDataModel):
    message: str
    status: HTTPStatus

    def to_dict(self) -> dict:
        return self.model_dump(mode="json")
