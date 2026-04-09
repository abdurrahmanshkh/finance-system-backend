from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator
from app.models.transaction import TransactionType

class TransactionBase(BaseModel):
    # gt=0 ensures the amount is strictly greater than 0
    amount: float = Field(..., gt=0, description="Amount must be greater than zero")
    type: TransactionType
    category: str = Field(..., min_length=1, description="Category cannot be empty")
    date: date
    notes: Optional[str] = None

    # Custom Validator: Prevent future dates for transactions
    @field_validator('date')
    @classmethod
    def validate_date_not_in_future(cls, value: date) -> date:
        if value > date.today():
            raise ValueError("Transaction date cannot be in the future.")
        return value

class TransactionCreate(TransactionBase):
    pass

# For updates, all fields are optional, so the user can update just one field (like notes)
class TransactionUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[TransactionType] = None
    category: Optional[str] = Field(None, min_length=1)
    date: Optional[date] = None
    notes: Optional[str] = None

    @field_validator('date')
    @classmethod
    def validate_date_not_in_future(cls, value: Optional[date]) -> Optional[date]:
        if value and value > date.today():
            raise ValueError("Transaction date cannot be in the future.")
        return value

# Output schema
class TransactionResponse(TransactionBase):
    id: int
    user_id: int

    model_config = ConfigDict(from_attributes=True)