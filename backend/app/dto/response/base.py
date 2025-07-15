from pydantic import BaseModel as BasePydanticModel


class BaseResponseDataModel(BasePydanticModel):
    class Config:
        extra = "ignore"
        use_enum_values = True
        populate_by_name = True
