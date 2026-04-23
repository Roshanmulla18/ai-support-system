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

# ========== TICKET SCHEMAS ==========

class TicketBase(BaseModel):
    """Base ticket schema"""
    title: str
    description: str
    priority: Optional[str] = "medium"
    status: Optional[str] = "open"

class TicketCreate(BaseModel):
    """Ticket creation schema (from customer)"""
    title: str
    description: str
    priority: Optional[str] = "medium"
    
    @validator('title')
    def validate_title(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Title cannot be empty')
        if len(v) > 200:
            raise ValueError('Title cannot exceed 200 characters')
        return v
    
    @validator('description')
    def validate_description(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('Description cannot be empty')
        if len(v) > 5000:
            raise ValueError('Description cannot exceed 5000 characters')
        return v
    
    @validator('priority')
    def validate_priority(cls, v):
        if v and v not in ['low', 'medium', 'high', 'urgent']:
            raise ValueError('Priority must be one of: low, medium, high, urgent')
        return v

class TicketUpdate(BaseModel):
    """Ticket update schema (for agents/admins)"""
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    assigned_to: Optional[int] = None
    ai_category: Optional[str] = None
    ai_confidence: Optional[int] = None
    sentiment_score: Optional[int] = None
    ai_suggested_response: Optional[str] = None
    resolved_by_ai: Optional[bool] = None
    
    @validator('status')
    def validate_status(cls, v):
        if v and v not in ['open', 'in_progress', 'resolved', 'closed']:
            raise ValueError('Status must be one of: open, in_progress, resolved, closed')
        return v
    
    @validator('priority')
    def validate_priority(cls, v):
        if v and v not in ['low', 'medium', 'high', 'urgent']:
            raise ValueError('Priority must be one of: low, medium, high, urgent')
        return v

class TicketResponse(BaseModel):
    """Ticket response schema"""
    id: int
    title: str
    description: str
    status: str
    priority: str
    user_id: int
    assigned_to: Optional[int] = None
    ai_category: Optional[str] = None
    ai_confidence: Optional[int] = None
    sentiment_score: Optional[int] = None
    ai_suggested_response: Optional[str] = None
    resolved_by_ai: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class TicketListResponse(BaseModel):
    """Paginated ticket list response"""
    total: int
    skip: int
    limit: int
    tickets: List[TicketResponse]

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