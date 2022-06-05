from datetime import date, datetime
from typing import Optional

from sqlalchemy import Column, Date, DateTime, func
from sqlmodel import Field, SQLModel


class Record(SQLModel, table=True):
    """Model for one day record in diary"""

    # default None + primary key means auto-increment of ID
    id: int = Field(default=None, primary_key=True, index=True)
    date_of_record: date = Field(sa_column=Column(Date, nullable=False, unique=True, index=True))
    title: Optional[str] = Field(max_length=200)
    text: str
    created: datetime = Field(sa_column=Column(DateTime(True), nullable=False, server_default=func.now()))
