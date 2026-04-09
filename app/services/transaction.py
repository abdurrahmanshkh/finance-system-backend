from datetime import date
from typing import Optional, List
from sqlalchemy.orm import Session
from app.models.transaction import Transaction, TransactionType
from app.schemas.transaction import TransactionCreate, TransactionUpdate

def create_transaction(db: Session, obj_in: TransactionCreate, user_id: int) -> Transaction:
    # Convert Pydantic model to dictionary and append the owner's user_id
    db_obj = Transaction(**obj_in.model_dump(), user_id=user_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_transaction(db: Session, transaction_id: int, user_id: int) -> Optional[Transaction]:
    # Ensures a user can only fetch their OWN transaction
    return db.query(Transaction).filter(
        Transaction.id == transaction_id, 
        Transaction.user_id == user_id
    ).first()

def get_transactions(
    db: Session, 
    user_id: int, 
    skip: int = 0, 
    limit: int = 100,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    transaction_type: Optional[TransactionType] = None,
    category: Optional[str] = None
) -> List[Transaction]:
    
    # Start base query filtered by the current user
    query = db.query(Transaction).filter(Transaction.user_id == user_id)
    
    # Apply robust filtering if query parameters are provided
    if start_date:
        query = query.filter(Transaction.date >= start_date)
    if end_date:
        query = query.filter(Transaction.date <= end_date)
    if transaction_type:
        query = query.filter(Transaction.type == transaction_type)
    if category:
        # ilike provides case-insensitive matching
        query = query.filter(Transaction.category.ilike(f"%{category}%"))
        
    # Apply pagination and order by date descending (newest first)
    return query.order_by(Transaction.date.desc()).offset(skip).limit(limit).all()

def update_transaction(db: Session, db_obj: Transaction, obj_in: TransactionUpdate) -> Transaction:
    # exclude_unset=True ensures we only update fields the user actually sent
    update_data = obj_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(db_obj, field, value)
        
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_transaction(db: Session, db_obj: Transaction) -> None:
    db.delete(db_obj)
    db.commit()