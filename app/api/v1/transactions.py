from datetime import date
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.models.transaction import TransactionType
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse
from app.services import transaction as transaction_service

router = APIRouter()

@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
    transaction_in: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new financial record for the logged-in user."""
    return transaction_service.create_transaction(db=db, obj_in=transaction_in, user_id=current_user.id)


@router.get("/", response_model=List[TransactionResponse])
def read_transactions(
    skip: int = Query(0, ge=0, description="Pagination offset"),
    limit: int = Query(100, ge=1, le=1000, description="Max records to return"),
    start_date: Optional[date] = Query(None, description="Filter by start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Filter by end date (YYYY-MM-DD)"),
    type: Optional[TransactionType] = Query(None, description="Filter by income or expense"),
    category: Optional[str] = Query(None, description="Filter by category name"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retrieve multiple financial records with optional filtering and pagination."""
    # Ensure logical date range
    if start_date and end_date and start_date > end_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Start date cannot be after end date")
        
    return transaction_service.get_transactions(
        db=db, 
        user_id=current_user.id, 
        skip=skip, 
        limit=limit,
        start_date=start_date, 
        end_date=end_date, 
        transaction_type=type, 
        category=category
    )


@router.get("/{id}", response_model=TransactionResponse)
def read_transaction(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific financial record by ID."""
    transaction = transaction_service.get_transaction(db=db, transaction_id=id, user_id=current_user.id)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    return transaction


@router.put("/{id}", response_model=TransactionResponse)
def update_transaction(
    id: int,
    transaction_in: TransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing financial record."""
    transaction = transaction_service.get_transaction(db=db, transaction_id=id, user_id=current_user.id)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    
    return transaction_service.update_transaction(db=db, db_obj=transaction, obj_in=transaction_in)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a financial record."""
    transaction = transaction_service.get_transaction(db=db, transaction_id=id, user_id=current_user.id)
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    
    transaction_service.delete_transaction(db=db, db_obj=transaction)
    return None