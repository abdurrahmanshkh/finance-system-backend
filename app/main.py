from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.database import engine, Base
from app.models import user, transaction 

# Import Limiter and Middleware
from app.core.limiter import limiter
from app.core.middleware import AuditLogMiddleware

# Import the routers
from app.api.v1 import auth, transactions, analytics

Base.metadata.create_all(bind=engine)

tags_metadata = [
    {"name": "Authentication", "description": "Operations with users and login logic."},
    {"name": "Transactions", "description": "Manage financial records and CSV exports."},
    {"name": "Analytics", "description": "Advanced data aggregation (RBAC protected)."},
    {"name": "Health", "description": "Server status checks."}
]

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Backend API for tracking financial records, summaries, and analytics.",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    openapi_tags=tags_metadata
)

# 1. Add Rate Limiter State
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 2. Add Custom Audit Logging Middleware
app.add_middleware(AuditLogMiddleware)

# 3. Add CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Authentication"])
app.include_router(transactions.router, prefix=f"{settings.API_V1_STR}/transactions", tags=["Transactions"])
app.include_router(analytics.router, prefix=f"{settings.API_V1_STR}/analytics", tags=["Analytics"])

app.mount("/dashboard", StaticFiles(directory="static", html=True), name="static")

@app.get("/", tags=["Health"])
def root_check():
    return {"message": f"Welcome to the {settings.PROJECT_NAME}", "docs_url": "/docs"}

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "version": settings.VERSION}