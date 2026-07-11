from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models
from collections import defaultdict

def create_transaction(db: Session, transaction):

    new_transaction = models.Transaction(
        amount=transaction.amount,
        category=transaction.category,
        merchant=transaction.merchant,
        date=transaction.date,
        notes=transaction.notes,
        transaction_type=transaction.transaction_type
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction

def get_transactions(db: Session):
    return db.query(models.Transaction).all()

def delete_transactions(db: Session, transaction_id: int):
    transaction = (
        db.query(models.Transaction)
        .filter(models.Transaction.id == transaction_id)
        .first()
    )
    if transaction is None:
        return None
    db.delete(transaction)
    db.commit()

    return transaction

def update_transaction(db:Session, transaction_id: int, updated_data):
    transaction = (
        db.query(models.Transaction)
        .filter(models.Transaction.id == transaction_id)
        .first()
    )
    if transaction is None:
        return None
    
    transaction.amount = updated_data.amount
    transaction.category = updated_data.category
    transaction.merchant = updated_data.merchant
    transaction.date = updated_data.date
    transaction.notes = updated_data.notes,
    transaction.transaction_type = updated_data.transaction_type

    db.commit()
    db.refresh(transaction)

    return transaction

def get_summary(db: Session):

    transactions = db.query(models.Transaction).all()

    if not transactions:
        return {
            "total_income": 0,
            "total_expenses": 0,
            "balance": 0,
            "transaction_count": 0,
            "categories": {}
        }

    total_income = sum(
        t.amount for t in transactions
        if t.transaction_type == "income"
    )

    total_expenses = sum(
        t.amount for t in transactions
        if t.transaction_type == "expense"
    )

    categories = defaultdict(float)

    for transaction in transactions:
        if transaction.transaction_type == "expense":
            categories[transaction.category] += transaction.amount

    return {
        "total_income": round(total_income, 2),
        "total_expenses": round(total_expenses, 2),
        "balance": round(total_income - total_expenses, 2),
        "transaction_count": len(transactions),
        "categories": dict(categories)
    }
def filter_transactions(
        db: Session,
        start_date= None,
        end_date= None, 
        transaction_type= None,
        category= None
):
    query = db.query(models.Transaction)
    if start_date:
        query = query.filter(
            models.Transaction.date >= start_date
        )
    if end_date:
        query = query.filter(
            models.Transaction.date <= end_date
        )
    if transaction_type:
        query = query.filter(
            models.Transaction.transaction_type == transaction_type
        )

    if category:
        query = query.filter(
            models.Transaction.category == category
        )

    return query.all()

def get_monthly_summary(db: Session, year: int, month: int):

    month_string = f"{year}-{month:02d}"

    transactions = (
        db.query(models.Transaction)
        .filter(
            func.strftime(
                "%Y-%m",
                models.Transaction.date
            ) == month_string
        )
        .all()
    )

    if not transactions:
        return {
            "month": month_string,
            "income": 0,
            "expenses": 0,
            "balance": 0,
            "transaction_count": 0,
            "top_category": None
        }

    income = sum(
        t.amount for t in transactions
        if t.transaction_type == "income"
    )

    expenses = sum(
        t.amount for t in transactions
        if t.transaction_type == "expense"
    )

    categories = defaultdict(float)

    for transaction in transactions:
        if transaction.transaction_type == "expense":
            categories[transaction.category] += transaction.amount

    top_category = None

    if categories:
        top_category = max(
            categories,
            key=categories.get
        )

    return {
        "month": month_string,
        "income": round(income, 2),
        "expenses": round(expenses, 2),
        "balance": round(income - expenses, 2),
        "transaction_count": len(transactions),
        "top_category": top_category
    }