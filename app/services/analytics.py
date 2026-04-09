from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.transaction import Transaction, TransactionType

def get_summary(db: Session, user_id: int) -> dict:
    # Calculate total income
    income = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id, 
        Transaction.type == TransactionType.income
    ).scalar() or 0.0  # scalar() returns the single value, defaults to 0.0 if None

    # Calculate total expense
    expense = db.query(func.sum(Transaction.amount)).filter(
        Transaction.user_id == user_id, 
        Transaction.type == TransactionType.expense
    ).scalar() or 0.0

    return {
        "total_income": income,
        "total_expense": expense,
        "current_balance": income - expense
    }

def get_category_breakdown(db: Session, user_id: int):
    # Group by category and type, then sum the amounts
    results = db.query(
        Transaction.category,
        Transaction.type,
        func.sum(Transaction.amount).label("total_amount")
    ).filter(Transaction.user_id == user_id).group_by(Transaction.category, Transaction.type).all()
    
    return [
        {"category": row.category, "type": row.type, "total_amount": row.total_amount}
        for row in results
    ]

def get_monthly_breakdown(db: Session, user_id: int):
    # SQLite uses strftime to extract the Year-Month. 
    # Note: If migrating to PostgreSQL later, this function changes to func.to_char()
    results = db.query(
        func.strftime('%Y-%m', Transaction.date).label("month"),
        Transaction.type,
        func.sum(Transaction.amount).label("total_amount")
    ).filter(Transaction.user_id == user_id).group_by("month", Transaction.type).all()

    # The query returns separate rows for income and expense per month. 
    # We need to combine them into a single dictionary per month.
    monthly_data = {}
    for row in results:
        month = row.month
        if month not in monthly_data:
            monthly_data[month] = {"month": month, "total_income": 0.0, "total_expense": 0.0}
            
        if row.type == TransactionType.income:
            monthly_data[month]["total_income"] = row.total_amount
        else:
            monthly_data[month]["total_expense"] = row.total_amount

    # Convert the dictionary values back to a list, sorted by month
    return sorted(list(monthly_data.values()), key=lambda x: x["month"])