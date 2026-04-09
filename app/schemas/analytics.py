from pydantic import BaseModel
from typing import List
from app.models.transaction import TransactionType

# Schema for the basic top-level summary
class SummaryResponse(BaseModel):
    total_income: float
    total_expense: float
    current_balance: float

# Schema for the category breakdown list items
class CategoryBreakdown(BaseModel):
    category: str
    type: TransactionType
    total_amount: float

# Schema for the monthly historical breakdown list items
class MonthlyBreakdown(BaseModel):
    month: str  # Format: "YYYY-MM"
    total_income: float
    total_expense: float