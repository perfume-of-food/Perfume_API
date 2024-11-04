from enum import Enum
from pydantic import BaseModel
from .perfume import Perfume

class PrintStatus(str, Enum):
    PRINTING = "PRINTING"
    COMPLETED = "COMPLETED"
    NOT_FOUND = "NOT_FOUND"


class PrintRequest(BaseModel):
    task_id: int
    perfume: Perfume
    customerName: str


class PrintResponse(BaseModel):
    message: str
    task_id: int


class PrintStatusResponse(BaseModel):
    task_id: int
    status: PrintStatus 