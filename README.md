# Finance System API 🚀

A robust, Python-powered backend finance tracking system designed to manage and analyze personal financial records. Built with modern, asynchronous Python standards using FastAPI.

## Overview
This project is a RESTful API that allows users to securely register, log in, and manage their income and expenses. It features Role-Based Access Control (RBAC), database aggregations for financial summaries, and security layers like rate limiting and audit logging.

## Tech Stack
* **Framework:** FastAPI (Python 3.12)
* **Database:** SQLite (via SQLAlchemy 2.0 ORM)
* **Data Validation:** Pydantic V2
* **Authentication:** JWT (JSON Web Tokens) & bcrypt
* **Security:** SlowAPI (Rate Limiting)

## Key Features Built
1. **CRUD Operations:** Full management of financial transactions with advanced filtering capabilities (by date, type, category).
2. **Analytics Engine:** SQL-level data aggregation for top-level summaries, category-wise breakdowns, and month-by-month historical data.
3. **Role-Based Access Control (RBAC):**
   * `Viewer`: Can manage own records and view basic summaries.
   * `Analyst` / `Admin`: Granted access to advanced monthly and categorical analytics.
4. **Data Export:** Dynamically stream user records into a downloadable `.csv` file.
5. **Security & Reliability:**
   * Custom middleware for **Audit Logging** (tracks IPs, URLs, and execution times).
   * **Rate Limiting** on authentication endpoints to prevent brute-force attacks.
   * Comprehensive data validation ensuring financial integrity (e.g., no future dates, strictly positive amounts).

## Local Setup & Execution

**1. Clone & Activate Environment**
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
````

**2. Install Dependencies**

```bash
pip install -r requirements.txt
```

**3. Seed the Database (Highly Recommended)**
To save time during evaluation, a seed script is provided. It creates the database structure, sets up 3 test users, and generates 90 days of randomized financial records.

```bash
python seed.py
```

**4. Start the Server**

```bash
uvicorn app.main:app --reload
```

## How to Test the API

FastAPI automatically generates an interactive Swagger UI. Once the server is running, navigate to:
👉 **[http://127.0.0.1:8000/docs](https://www.google.com/url?sa=E&source=gmail&q=http://127.0.0.1:8000/docs)**

### Test Accounts (If Seeded)

Use the green **"Authorize"** button at the top right of the Swagger UI to log in.

  * **Admin:** `admin_user` / `password123`
  * **Analyst:** `analyst_user` / `password123` (Try the `/analytics/monthly-breakdown` endpoint)
  * **Viewer:** `viewer_user` / `password123` (Try accessing advanced analytics to see the `403 Forbidden` response)

## Architectural & Design Assumptions

  * **Database Choice:** SQLite was chosen strictly for portability and ease of assessment. Because the data layer relies entirely on SQLAlchemy ORM, migrating to PostgreSQL in a production environment requires only changing the connection string in `config.py`.
  * **Service Layer Pattern:** The project separates HTTP routing (`app/api`) from business logic and database queries (`app/services`). This ensures the code remains highly testable and maintainable as it scales.
  * **Timezones:** Dates are stored as standard `YYYY-MM-DD`. For a global production app, this would be upgraded to UTC timestamps.

-----

**Author:** Abdur Rehman Shaikh