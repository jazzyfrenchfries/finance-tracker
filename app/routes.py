from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud
from sqlalchemy import func
from typing import Dict,Any
from .schemas import CreateTransaction, TransactionResponse, TransactionType
from .database import SessionLocal
from datetime import date
from typing import Optional
from .schemas import SettingsUpdate, SettingsResponse

router = APIRouter()
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
@router.post("/transactions", response_model=TransactionResponse)
def create_transaction(
    transaction: CreateTransaction,
    db: Session = Depends(get_db)
):
    return crud.create_transaction(db, transaction)
@router.get("/transactions", response_model=list[TransactionResponse])
def read_transaction(
        db: Session = Depends(get_db)
):
    return crud.get_transactions(db)
@router.delete("/transactions/{transaction_id}", response_model=TransactionResponse)
def delete_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    deleted_transaction = crud.delete_transactions(db, transaction_id)
    if deleted_transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return deleted_transaction
@router.put("/transactions/{transaction_id}", response_model=TransactionResponse)
def update_transaction(
    transaction_id: int,
    transaction: CreateTransaction,
    db: Session = Depends(get_db)
):
    updated_transaction = crud.update_transaction(
        db,
        transaction_id,
        transaction
    )

    if updated_transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaction not found"
        )

    return updated_transaction
@router.get("/balance")
def balance(
    db: Session = Depends(get_db)
):
    return crud.get_balance(db)

@router.get(
    "/transactions/filter",
    response_model=list[TransactionResponse]
)
def filter_transactions(
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    transaction_type: Optional[TransactionType] = None,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return crud.filter_transactions(
        db,
        start_date,
        end_date,
        transaction_type,
        category
    )

@router.get("/summary/monthly")
def monthly_summary(
    year: int,
    month: int,
    db: Session = Depends(get_db)
):
    return crud.get_monthly_summary(
        db,
        year,
        month
    )

@router.get(
    "/settings",
    response_model=SettingsResponse
)
def get_settings(
    db: Session = Depends(get_db)
):
    return crud.get_settings(db)



@router.put(
    "/settings",
    response_model=SettingsResponse
)
def update_settings(
    settings: SettingsUpdate,
    db: Session = Depends(get_db)
):
    return crud.update_settings(
        db,
        settings.opening_balance
    )