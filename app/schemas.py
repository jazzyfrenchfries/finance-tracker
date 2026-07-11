from pydantic import BaseModel, ConfigDict 
from datetime import date
from typing import Optional
from enum import Enum
class TransactionType(str,Enum):
    income = "income"
    expense = "expense"
class  CreateTransaction(BaseModel):
    amount: float
    category: str
    merchant: str
    date: date
    notes: Optional[str] = None
    transaction_type : TransactionType

class TransactionResponse(BaseModel):
    id: int 
    amount: float
    category: str
    merchant: str
    date: date
    notes: Optional[str] = None
    transaction_type: TransactionType 

    model_config = ConfigDict(from_attributes = True)