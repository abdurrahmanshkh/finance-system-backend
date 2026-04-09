import enum
from datetime import date
from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.core.database import Base

class TransactionType(str, enum.Enum):
    income = "income"
    expense = "expense"

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    type = Column(Enum(TransactionType), nullable=False)
    category = Column(String, index=True, nullable=False)
    date = Column(Date, default=date.today, nullable=False)
    notes = Column(String, nullable=True)
    
    # Foreign Key linking to the users table
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relationship back to the User model
    owner = relationship("User", back_populates="transactions")