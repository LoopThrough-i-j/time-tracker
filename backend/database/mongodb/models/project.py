from datetime import datetime

from pydantic import Field

from database.constants.collections import DatabaseCollections
from database.mongodb.models.base import BaseMongoModel


class Payroll(BaseMongoModel):
    bill_rate: float = Field(alias="billRate")
    overtime_billrate: float = Field(alias="overtimeBillrate")


class Project(BaseMongoModel):
    collection = DatabaseCollections.PROJECTS

    name: str = Field()
    description: str = Field()
    employees: list[str] = Field(default_factory=list)
    statuses: list[str] = Field(default_factory=list)
    priorities: list[str] = Field(default_factory=list)
    billable: bool = Field(default=False)
    deadline: datetime | None = Field(default=None)
    payroll: Payroll | None = Field(default=None)
    archived: bool = Field(default=False)
    creator_id: str = Field(alias="creatorId")
    organization_id: str = Field(alias="organizationId")
    teams: list[str] = Field(default_factory=list)
