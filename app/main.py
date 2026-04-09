from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# Initialize FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Backend API for tracking financial records, summaries, and analytics.",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS (Cross-Origin Resource Sharing)
# This allows a frontend application to communicate with this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, replace "*" with specific frontend domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health"])
def root_check():
    return {
        "message": f"Welcome to the {settings.PROJECT_NAME}",
        "docs_url": "/docs"
    }

@app.get("/health", tags=["Health"])
def health_check():
    """
    Endpoint to verify that the API is up and running.
    """
    return {
        "status": "healthy",
        "version": settings.VERSION
    }