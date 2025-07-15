from pydantic import BaseModel


class Tag(BaseModel):
    name: str
    description: str = str()


class APITags:
    EMPLOYEE = Tag(name="Employee", description="Employee management operations")
    PROJECT = Tag(name="Project", description="Project management operations")
    TASK = Tag(name="Task", description="Task management operations")
    TIME_LOG = Tag(name="TimeLog", description="Time tracking and analytics operations")

    @classmethod
    def to_list(cls):
        return [v.model_dump() for k, v in cls.__dict__.items() if isinstance(v, Tag)]
