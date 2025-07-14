from datetime import datetime
from enum import Enum

from pydantic import EmailStr, Field

from database.constants.collections import DatabaseCollections
from database.mongodb.models.base import BaseMongoModel


class EmployeeType(str, Enum):
    PERSONAL = "personal"
    OFFICE = "office"


class Employee(BaseMongoModel):
    collection = DatabaseCollections.EMPLOYEES

    name: str = Field()
    email: EmailStr = Field()
    team_id: str = Field()
    identifier: str = Field()
    type: EmployeeType = Field(default=EmployeeType.PERSONAL)
    projects: list[str] = Field(default_factory=list)
    invited_at: datetime = Field()
