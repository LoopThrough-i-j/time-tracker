from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from typing import Any, ClassVar
from uuid import uuid4

from pydantic import BaseModel as BasePydanticModel, Field


class BaseDataModel(BasePydanticModel):
    class Config:
        extra = "ignore"
        validate_default = True
        arbitrary_types_allowed = True
        populate_by_name = True

    def model_dump_db(self) -> dict[str, Any]:
        python_model_dump = super().model_dump(mode="python", by_alias=True)
        return self._custom_dict(python_model_dump)

    def _custom_dict(self, value: Any) -> Any:
        if isinstance(value, Decimal):
            return float(value)

        if isinstance(value, dict):
            return {self._custom_dict(k): self._custom_dict(v) for k, v in value.items()}

        if isinstance(value, list):
            return [self._custom_dict(i) for i in value]

        if isinstance(value, Enum):
            return value.value

        return value


class BaseMongoModel(BaseDataModel):
    collection: ClassVar = ""

    id: str = Field(default_factory=lambda: f"id_{uuid4().hex}", alias="_id")

    is_active: bool = True
    is_deleted: bool = False

    created_by: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_by: str | None = None
    updated_at: datetime | None = None
