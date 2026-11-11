from pydantic import BaseModel


class DatabaseStatus(BaseModel):
    enabled: bool
    connected: bool
    detail: str
