import logging
import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError
from app.core.config import settings

# Configure standard Python logging to write to a file
logging.basicConfig(
    filename="audit.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

class AuditLogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # Attempt to identify the user from the Authorization header
        user_identity = "Anonymous"
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
                user_identity = payload.get("sub", "Unknown User")
            except JWTError:
                user_identity = "Invalid Token"

        # Process the request
        response = await call_next(request)
        
        # Calculate execution time
        process_time = time.time() - start_time
        
        # Log the audit record
        log_message = (
            f"User: {user_identity} | "
            f"Method: {request.method} | "
            f"Path: {request.url.path} | "
            f"Status: {response.status_code} | "
            f"IP: {request.client.host} | "
            f"Time: {process_time:.4f}s"
        )
        logger.info(log_message)
        
        return response