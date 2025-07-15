from datetime import datetime

from pydantic import Field

from database.constants.collections import DatabaseCollections
from database.mongodb.models.base import BaseMongoModel


class Task(BaseMongoModel):
    collection = DatabaseCollections.TASKS

    name: str | None = Field(default=None)
    description: str | None = Field(default=None)
    employees: list[str] = Field(default_factory=list)
    project_id: str = Field()
    deadline: datetime | None = Field(default=None)
    status: str | None = Field(default=None)
    labels: list[str] = Field(default_factory=list)
    priority: str | None = Field(default=None)
    billable: bool = Field(default=True)
