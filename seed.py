import random
from datetime import date, timedelta
from app.core.database import SessionLocal, engine, Base
from app.models.user import User, UserRole
from app.models.transaction import Transaction, TransactionType
from app.core.security import get_password_hash

def seed_database():
    print("Dropping existing tables and recreating (Resetting database)...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        print("Creating test users...")
        users_data = [
            {"username": "admin_user", "password": "password123", "role": UserRole.admin},
            {"username": "analyst_user", "password": "password123", "role": UserRole.analyst},
            {"username": "viewer_user", "password": "password123", "role": UserRole.viewer},
        ]

        db_users = {}
        for u in users_data:
            user = User(
                username=u["username"],
                hashed_password=get_password_hash(u["password"]),
                role=u["role"]
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            db_users[u["role"]] = user
            print(f"  -> Created {u['role'].value}: {u['username']} / password123")

        print("Generating realistic transaction data...")
        categories_expense = ["Rent", "Groceries", "Utilities", "Entertainment", "Transportation"]
        categories_income = ["Salary", "Freelance", "Dividends"]

        # Generate data for the last 90 days
        today = date.today()
        
        # Populate transactions for Analyst and Viewer
        for role in [UserRole.analyst, UserRole.viewer]:
            user = db_users[role]
            for i in range(30): # 30 transactions per user
                # Random date within the last 90 days
                txn_date = today - timedelta(days=random.randint(0, 90))
                
                # 70% chance of expense, 30% chance of income
                if random.random() > 0.3:
                    txn_type = TransactionType.expense
                    category = random.choice(categories_expense)
                    amount = round(random.uniform(10.0, 500.0), 2)
                else:
                    txn_type = TransactionType.income
                    category = random.choice(categories_income)
                    amount = round(random.uniform(1000.0, 3000.0), 2)

                txn = Transaction(
                    amount=amount,
                    type=txn_type,
                    category=category,
                    date=txn_date,
                    notes=f"Auto-generated {category} record",
                    user_id=user.id
                )
                db.add(txn)

        db.commit()
        print("Database successfully seeded! Ready for testing.")

    except Exception as e:
        print(f"An error occurred: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()