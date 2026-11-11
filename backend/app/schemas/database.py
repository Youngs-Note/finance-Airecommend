from pydantic import BaseModel


class MySQLStatus(BaseModel):
    enabled: bool
    connected: bool
    detail: str
