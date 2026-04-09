# Finance System API & Dashboard 🚀

A robust, Python-powered finance tracking system designed to manage and analyze personal financial records. Built with modern, asynchronous Python standards using FastAPI, complete with a beautifully integrated Vanilla JS and Tailwind CSS frontend dashboard.

## Overview
This project serves as a comprehensive finance management tool. The backend is a secure RESTful API featuring Role-Based Access Control (RBAC), database aggregations, and robust security layers. The frontend provides a seamless, interactive Single Page Application (SPA) to visualize analytics and manage records in real-time.

## Tech Stack
**Backend:**
* **Framework:** FastAPI (Python 3.12)
* **Database:** SQLite (via SQLAlchemy 2.0 ORM)
* **Data Validation:** Pydantic V2
* **Authentication:** JWT (JSON Web Tokens) & bcrypt
* **Security:** SlowAPI (Rate Limiting)

**Frontend:**
* **UI/UX:** Vanilla JavaScript, HTML5
* **Styling:** Tailwind CSS (via CDN)
* **Icons:** FontAwesome

## Key Features Built
1. **Interactive Dashboard:** A modern, responsive UI hosted directly from the API that allows users to log in, view real-time summary statistics, and manage transactions seamlessly.
2. **CRUD Operations:** Full management of financial transactions with advanced filtering capabilities (by date, type, category).
3. **Analytics Engine:** SQL-level data aggregation for top-level summaries, category-wise breakdowns, and month-by-month historical data.
4. **Role-Based Access Control (RBAC):**
   * `Viewer`: Can manage own records and view basic summaries.
   * `Analyst` / `Admin`: Granted access to advanced monthly and categorical analytics.
5. **Data Export:** Dynamically stream user records into a downloadable `.csv` file directly from the UI or API.
6. **Security & Reliability:**
   * Custom middleware for **Audit Logging** (tracks IPs, URLs, and execution times).
   * **Rate Limiting** on authentication endpoints to prevent brute-force attacks.
   * Comprehensive data validation ensuring financial integrity (e.g., no future dates, strictly positive amounts).

## Local Setup & Execution

**1. Clone & Activate Environment**
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows PowerShell
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

## How to Test the Application

### Option A: The User Dashboard (Frontend)

Experience the application as a user. Once the server is running, navigate to:
👉 **[http://127.0.0.1:8000/dashboard/](https://www.google.com/search?q=http://127.0.0.1:8000/dashboard/)**

### Option B: The API Documentation (Backend)

Test the raw API endpoints and explore the schema definitions via the interactive Swagger UI:
👉 **[http://127.0.0.1:8000/docs](https://www.google.com/search?q=http://127.0.0.1:8000/docs)**

### Test Accounts (If Seeded)

Use these credentials to log in to either the Dashboard or the Swagger UI:

  * **Admin:** `admin_user` / `password123`
  * **Analyst:** `analyst_user` / `password123`
  * **Viewer:** `viewer_user` / `password123` *(Note: Viewers will be blocked from accessing advanced analytics endpoints).*

## Architectural & Design Assumptions

  * **Full-Stack Integration:** To avoid requiring a Node.js/npm setup for the reviewer, the frontend is built as a lightweight SPA served as static files directly by FastAPI.
  * **Database Choice:** SQLite was chosen strictly for portability and ease of assessment. Because the data layer relies entirely on SQLAlchemy ORM, migrating to PostgreSQL in a production environment requires only changing the connection string in `config.py`.
  * **Service Layer Pattern:** The backend separates HTTP routing (`app/api`) from business logic and database queries (`app/services`). This ensures the code remains highly testable and maintainable as it scales.

-----

**Author:** Abdur Rehman Shaikh