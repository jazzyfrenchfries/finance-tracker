from sqlalchemy import Column, Integer,String,Float,Date
from .database import Base
class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer,primary_key=True,index=True)
    amount = Column(Float, nullable=False)
    category = Column(String, nullable=False)
    merchant = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    notes = Column(String, nullable=True)