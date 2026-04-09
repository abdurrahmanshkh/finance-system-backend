from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user, RoleChecker
from app.models.user import User, UserRole
from app.schemas.analytics import SummaryResponse, CategoryBreakdown, MonthlyBreakdown
from app.services import analytics as analytics_service

router = APIRouter()

# Allow basic summary for ANY logged-in user
@router.get("/summary", response_model=SummaryResponse)
def read_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get the top-level financial summary (Total Income, Total Expense, Balance)."""
    return analytics_service.get_summary(db=db, user_id=current_user.id)


# Restrict advanced insights to Analysts and Admins using our RoleChecker
allow_analyst_and_admin = RoleChecker([UserRole.analyst, UserRole.admin])

@router.get("/category-breakdown", response_model=List[CategoryBreakdown])
def read_category_breakdown(
    db: Session = Depends(get_db),
    # The Depends(allow_analyst_and_admin) handles both authentication AND authorization
    current_user: User = Depends(allow_analyst_and_admin) 
):
    """
    Get a breakdown of transactions by category. 
    **Requires Analyst or Admin role.**
    """
    return analytics_service.get_category_breakdown(db=db, user_id=current_user.id)


@router.get("/monthly-breakdown", response_model=List[MonthlyBreakdown])
def read_monthly_breakdown(
    db: Session = Depends(get_db),
    current_user: User = Depends(allow_analyst_and_admin)
):
    """
    Get a month-by-month historical breakdown of income and expenses.
    **Requires Analyst or Admin role.**
    """
    return analytics_service.get_monthly_breakdown(db=db, user_id=current_user.id)