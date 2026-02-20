"""
main.py - AutoResolve AI Phase 3 COMPLETE
Production-ready authentication system with login and protected routes
"""

from fastapi import FastAPI, Depends, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from sqlalchemy import func, text
from datetime import datetime, timedelta
from typing import List, Optional
from pydantic import BaseModel, validator, Field
import hashlib
import re
import os
from dotenv import load_dotenv

# Import local modules
import models
import database
import auth
import schemas

# Load environment variables
load_dotenv()

# Create tables
try:
    models.Base.metadata.create_all(bind=database.engine)
    print("✅ Tables created successfully")
except Exception as e:
    print(f"❌ Error creating tables: {e}")

app = FastAPI(
    title="AutoResolve AI",
    description="Production-ready authentication system with complete user management",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== REQUEST/RESPONSE SCHEMAS ==========

class UserCreate(BaseModel):
    email: str
    username: str = Field(..., min_length=3, max_length=20)
    password: str
    full_name: Optional[str] = None
    
    # Email validation
    @validator('email')
    def validate_email(cls, v):
        v = v.lower().strip()
        if '@' not in v:
            raise ValueError('Email must contain @ symbol')
        
        parts = v.split('@')
        if len(parts) != 2:
            raise ValueError('Email must have exactly one @ symbol')
        
        local, domain = parts
        
        if not local:
            raise ValueError('Email must have text before @')
        if not domain:
            raise ValueError('Email must have text after @')
        if local.startswith('.') or local.endswith('.'):
            raise ValueError('Email cannot start or end with dot')
        if '..' in local:
            raise ValueError('Email cannot have consecutive dots')
        if domain.startswith('.') or domain.startswith('-'):
            raise ValueError('Domain cannot start with dot or hyphen')
        if domain.endswith('.'):
            raise ValueError('Domain cannot end with dot')
        if '..' in domain:
            raise ValueError('Domain cannot have consecutive dots')
        if ' ' in v:
            raise ValueError('Email cannot contain spaces')
        if '.' not in domain:
            raise ValueError('Domain must have a dot')
        if ',' in domain:
            raise ValueError('Domain must use dots, not commas')
        
        domain_parts = domain.split('.')
        if len(domain_parts[-1]) < 2:
            raise ValueError('Domain ending must be at least 2 characters')
        
        return v
    
    # Username validation
    @validator('username')
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username can only contain letters, numbers, and underscore')
        if '__' in v:
            raise ValueError('Username cannot have consecutive underscores')
        if v.startswith('_') or v.endswith('_'):
            raise ValueError('Username cannot start or end with underscore')
        return v
    
    # Password validation
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if len(v) > 72:
            raise ValueError('Password cannot exceed 72 characters')
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain at least one number')
        return v

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str] = None
    role: str
    is_active: bool
    created_at: Optional[str] = None
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class LoginRequest(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    password: Optional[str] = None

# ========== PUBLIC ENDPOINTS ==========

@app.get("/")
def root():
    """Root endpoint with API information"""
    return {
        "project": "AutoResolve AI",
        "version": "1.0.0",
        "status": "production",
        "phase": "Phase 3 - Complete",
        "endpoints": {
            "GET /": "This information",
            "GET /test": "Health check",
            "GET /health": "Detailed health check",
            "POST /register": "Create new account",
            "POST /login": "Login and get JWT token",
            "GET /users/me": "Get current user (protected)",
            "PUT /users/me": "Update current user (protected)",
            "GET /docs": "API documentation"
        }
    }

@app.get("/test")
def test(db: Session = Depends(database.get_db)):
    """Simple health check endpoint"""
    try:
        db.execute(text("SELECT 1")).first()
        return {
            "success": True,
            "database": "connected",
            "message": "API is working"
        }
    except Exception as e:
        return {
            "success": False,
            "database": "error",
            "error": str(e)
        }

@app.get("/health")
def health_check(db: Session = Depends(database.get_db)):
    """Detailed health check endpoint"""
    try:
        db.execute(text("SELECT 1")).first()
        db_status = "healthy"
    except Exception as e:
        db_status = f"unhealthy: {str(e)}"
    
    # Get user count
    try:
        user_count = db.query(models.User).count()
    except:
        user_count = 0
    
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "database": db_status,
        "user_count": user_count,
        "version": "1.0.0"
    }

# ========== REGISTRATION ENDPOINT ==========

@app.post("/register", response_model=UserResponse, status_code=201)
def register(user: UserCreate, db: Session = Depends(database.get_db)):
    """
    Register a new user with complete validation
    
    Validation rules:
    - Email: Valid format, case-insensitive, no duplicates
    - Username: 3-20 chars, alphanumeric + underscore
    - Password: 8-72 chars, uppercase, lowercase, number
    """
    try:
        # Check if email exists (case-insensitive)
        existing_email = db.query(models.User).filter(
            func.lower(models.User.email) == user.email.lower()
        ).first()
        
        if existing_email:
            raise HTTPException(400, "Email already registered")
        
        # Check if username exists
        existing_username = db.query(models.User).filter(
            models.User.username == user.username
        ).first()
        
        if existing_username:
            raise HTTPException(400, "Username already taken")
        
        # Create user with hashed password
        hashed_password = auth.get_password_hash(user.password)
        
        db_user = models.User(
            email=user.email,
            username=user.username,
            full_name=user.full_name,
            hashed_password=hashed_password,
            role="customer",
            is_active=True
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Convert datetime to string for response
        response_data = {
            "id": db_user.id,
            "email": db_user.email,
            "username": db_user.username,
            "full_name": db_user.full_name,
            "role": db_user.role,
            "is_active": db_user.is_active,
            "created_at": db_user.created_at.isoformat() if db_user.created_at else None
        }
        
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Registration error: {e}")
        raise HTTPException(500, f"Internal server error")

# ========== LOGIN ENDPOINT ==========

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    """
    Login with username/email and password to get JWT token
    
    Returns:
    - access_token: JWT token for authentication
    - token_type: Bearer
    - expires_in: Token expiration in seconds
    """
    # Authenticate user
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username, "role": user.role, "user_id": user.id},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": auth.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

# ========== PROTECTED ENDPOINTS (Require Login) ==========

@app.get("/users/me", response_model=UserResponse)
def read_users_me(current_user = Depends(auth.get_current_active_user)):
    """Get current logged in user information"""
    if not current_user:
        raise HTTPException(401, "Not authenticated")
    
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None
    }

@app.put("/users/me", response_model=UserResponse)
def update_user_me(
    user_update: UserUpdate,
    db: Session = Depends(database.get_db),
    current_user = Depends(auth.get_current_active_user)
):
    """Update current user profile"""
    if not current_user:
        raise HTTPException(401, "Not authenticated")
    
    # Update email if provided
    if user_update.email:
        # Check if email already taken
        existing = db.query(models.User).filter(
            func.lower(models.User.email) == user_update.email.lower(),
            models.User.id != current_user.id
        ).first()
        if existing:
            raise HTTPException(400, "Email already registered")
        current_user.email = user_update.email
    
    # Update full name if provided
    if user_update.full_name:
        current_user.full_name = user_update.full_name
    
    # Update password if provided
    if user_update.password:
        if len(user_update.password) < 8:
            raise HTTPException(400, "Password must be at least 8 characters")
        current_user.hashed_password = auth.get_password_hash(user_update.password)
    
    db.commit()
    db.refresh(current_user)
    
    return {
        "id": current_user.id,
        "email": current_user.email,
        "username": current_user.username,
        "full_name": current_user.full_name,
        "role": current_user.role,
        "is_active": current_user.is_active,
        "created_at": current_user.created_at.isoformat() if current_user.created_at else None
    }

# ========== RUN SERVER ==========
if __name__ == "__main__":
    import uvicorn
    print("="*60)
    print("🚀 AUTORESOLVE AI - PHASE 3 COMPLETE")
    print("="*60)
    print("✅ Registration with full validation")
    print("✅ Login with JWT tokens")
    print("✅ Protected routes")
    print("✅ Case-insensitive email checking")
    print("✅ Password hashing with bcrypt")
    print("="*60)
    print("🌐 http://localhost:8001")
    print("📚 http://localhost:8001/docs")
    print("="*60)
    print("🔑 Test login with registered user")
    print("="*60)
    
    uvicorn.run(app, host="0.0.0.0", port=8001)