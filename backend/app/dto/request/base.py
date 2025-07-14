from pydantic import BaseModel


class BaseRequestModel(BaseModel):
    class Config:
        extra = "ignore"
        use_enum_values = True
