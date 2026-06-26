from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import crud
from .schemas import CreateTransaction
from .database import SessionLocal
router = APIRouter()
def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
@router.post("/transactions")
def create_transaction(
    transaction: CreateTransaction,
    db: Session = Depends(get_db)
):
    return crud.create_transaction(db, transaction)