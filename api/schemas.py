from datetime import date
from typing import Optional

from pydantic import BaseModel


class RecordCreate(BaseModel):
    """Model for creating a record. Contains only necessary information"""

    title: Optional[str] = None
    date: date
    text: str


class HTTP404Error(BaseModel):
    """Model of 404 error"""

    detail: str

    class Config:
        """Extra configuration of model"""

        schema_extra = {
            "example": {"detail": "Item not found"},
        }
