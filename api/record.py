from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import MultipleResultsFound, NoResultFound
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from api.schemas import HTTP404Error, RecordCreate
from database.database import get_session
from database.models import Record

records_router = APIRouter(
    prefix="/record",
    tags=["Record"],
)


@records_router.get(
    "/{id}",
    response_model=Record,
    status_code=200,
    summary="Get record from database",
    description="Get one record from database based on ID given.",
    responses={404: {"model": HTTP404Error, "description": "Record not found"}},
)
async def get_record(_id: int, db_session: AsyncSession = Depends(get_session)):
    """
    Get the record by given ID.

    Args:
        _id (int):
        db_session (AsyncSession): database session

    Returns:
        Record: Record found by given ID or HTTPException
    """
    query = select(Record).where(Record.id == _id).limit(1)
    result = await db_session.scalars(query)
    try:
        result = result.one()
    except NoResultFound as exc:
        raise HTTPException(status_code=404, detail="No Record found") from exc
    except MultipleResultsFound as exc:
        raise HTTPException(status_code=404, detail="Multiple Records found") from exc
    return result


@records_router.get(
    "",
    response_model=List[Record],
    status_code=200,
    summary="Get all records from database",
    description="Get all records in database and returns them as a list",
)
async def get_all_records(db_session: AsyncSession = Depends(get_session)):
    """
    Get all the records.

    Args:
        db_session (AsyncSession): database session

    Returns:
        List[Record]: All records in database.
    """
    query = select(Record)
    result = await db_session.scalars(query)
    result = result.all()
    return result


@records_router.post(
    "",
    response_model=Record,
    status_code=201,
    summary="Create new record",
    description="Takes necessary infromation to create a new record and creates it in database. Then returns the new "
    "record.",
)
async def create_record(record: RecordCreate, db_session: AsyncSession = Depends(get_session)):
    """
    Create new record in DB.

    Args:
        record (RecordCreate): record information for new record to be created.
        db_session (AsyncSession): database session

    Returns:
        Record: newly created record.
    """
    new_record = Record(date_of_record=record.date, title=record.title, text=record.text)
    db_session.add(new_record)
    await db_session.commit()
    await db_session.refresh(new_record)
    return new_record
