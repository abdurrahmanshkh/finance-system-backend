from pydantic import BaseModel, Field, ConfigDict
from app.models.user import UserRole

# Base properties shared across multiple user schemas
class UserBase(BaseModel):
    # Field(...) means the field is required. We also enforce length limits.
    username: str = Field(..., min_length=3, max_length=50, description="Unique username")
    role: UserRole = UserRole.viewer

# Schema for User Registration
class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters long")

# Schema for User Login
class UserLogin(BaseModel):
    username: str
    password: str

# Schema for returning user data (The "Profile" view)
class UserResponse(UserBase):
    id: int

    # ConfigDict(from_attributes=True) tells Pydantic to read data even if it's not a dict,
    # which is required for translating SQLAlchemy ORM models into JSON responses.
    model_config = ConfigDict(from_attributes=True)