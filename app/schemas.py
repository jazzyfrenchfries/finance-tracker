from pydantic import BaseModel 
from datetime import date
class  CreateTransaction(BaseModel):
    amount: float
    category: str
    merchant: str
    date: date
    notes: str