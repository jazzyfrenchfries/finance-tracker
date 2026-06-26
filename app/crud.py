from sqlalchemy.orm import Session
from . import models


def create_transaction(db: Session, transaction):

    new_transaction = models.Transaction(
        amount=transaction.amount,
        category=transaction.category,
        merchant=transaction.merchant,
        date=transaction.date,
        notes=transaction.notes
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction