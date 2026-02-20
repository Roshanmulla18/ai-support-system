"""
schemas.py - Pydantic schemas for data validation
"""

from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime

# ========== USER SCHEMAS ==========

class UserBase(BaseModel):
    """Base user schema"""
    email: str
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    """User creation schema"""
    password: str

class UserUpdate(BaseModel):
    """User update schema (all fields optional)"""
    email: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    """User response schema (excludes password)"""
    id: int
    email: str
    username: str
    full_name: Optional[str] = None
    role: str
    is_active: bool
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UserInDB(UserResponse):
    """User schema as stored in DB (includes hashed password)"""
    hashed_password: str

# ========== TOKEN SCHEMAS ==========

class Token(BaseModel):
    """JWT token response schema"""
    access_token: str
    token_type: str
    expires_in: int

class TokenData(BaseModel):
    """Data stored in JWT token"""
    username: Optional[str] = None
    role: Optional[str] = None
    user_id: Optional[int] = None

class LoginRequest(BaseModel):
    """Login request schema"""
    username: str
    password: str

# ========== HEALTH SCHEMAS ==========

class HealthResponse(BaseModel):
    """Health check response schema"""
    status: str
    timestamp: str
    database: str
    user_count: int
    version: str

# ========== ERROR SCHEMAS ==========

class ErrorResponse(BaseModel):
    """Error response schema"""
    detail: str

class ValidationErrorDetail(BaseModel):
    """Validation error detail schema"""
    loc: List[str]
    msg: str
    type: str

class ValidationErrorResponse(BaseModel):
    """Validation error response schema"""
    detail: List[ValidationErrorDetail]