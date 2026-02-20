"""
main.py - AutoResolve AI Phase 3 PRODUCTION READY
Complete validation with case-insensitive email checking
"""

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import func
import hashlib
import models
import database
from pydantic import BaseModel, validator, Field
from typing import Optional
import re

# Create tables
try:
    models.Base.metadata.create_all(bind=database.engine)
    print("✅ Tables created successfully")
except Exception as e:
    print(f"❌ Error creating tables: {e}")

app = FastAPI(title="AutoResolve AI")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========== COMPLETE VALIDATION SCHEMAS ==========

class UserCreate(BaseModel):
    email: str
    username: str = Field(..., min_length=3, max_length=20)
    password: str
    full_name: Optional[str] = None
    
    # ===== EMAIL VALIDATION (15 RULES + CASE INSENSITIVE) =====
    @validator('email')
    def validate_email(cls, v):
        original = v  # Keep for error messages
        
        # Rule 1: Check if email contains @
        if '@' not in v:
            raise ValueError('Email must contain @ symbol')
        
        # Rule 2: Split into local and domain parts
        parts = v.split('@')
        if len(parts) != 2:
            raise ValueError('Email must have exactly one @ symbol')
        
        local, domain = parts
        
        # Rule 3: Check if local part is not empty
        if not local:
            raise ValueError('Email must have text before @')
        
        # Rule 4: Check if domain is not empty
        if not domain:
            raise ValueError('Email must have text after @')
        
        # Rule 5: Local part cannot start or end with dot
        if local.startswith('.'):
            raise ValueError('Local part cannot start with dot')
        if local.endswith('.'):
            raise ValueError('Local part cannot end with dot')
        
        # Rule 6: No consecutive dots in local part
        if '..' in local:
            raise ValueError('Local part cannot have consecutive dots')
        
        # Rule 7: Domain cannot start with dot or hyphen
        if domain.startswith('.') or domain.startswith('-'):
            raise ValueError('Domain cannot start with dot or hyphen')
        
        # Rule 8: Domain must have at least one dot
        if '.' not in domain:
            raise ValueError('Domain must have a dot (e.g., gmail.com)')
        
        # Rule 9: Domain cannot end with dot
        if domain.endswith('.'):
            raise ValueError('Domain cannot end with dot')
        
        # Rule 10: No consecutive dots in domain
        if '..' in domain:
            raise ValueError('Domain cannot have consecutive dots')
        
        # Rule 11: Check for spaces anywhere
        if ' ' in v:
            raise ValueError('Email cannot contain spaces')
        
        # Rule 12: Domain should have at least one dot with text after
        domain_parts = domain.split('.')
        if len(domain_parts) < 2 or not all(domain_parts):
            raise ValueError('Email domain must be valid (e.g., gmail.com)')
        
        # Rule 13: TLD (last part) should be at least 2 characters
        tld = domain_parts[-1]
        if len(tld) < 2:
            raise ValueError('Domain ending (TLD) must be at least 2 characters')
        
        # Rule 14: Check for invalid characters (only letters, numbers, dots, hyphens allowed)
        allowed_chars = re.compile(r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        if not allowed_chars.match(v):
            raise ValueError('Email contains invalid characters. Only letters, numbers, dots, hyphens allowed')
        
        # Rule 15: Check for comma instead of dot
        if ',' in domain:
            raise ValueError('Domain must use dots (.), not commas (,)')
        
        # Return lowercase version for consistent storage
        return v.lower()
    
    # ===== USERNAME VALIDATION =====
    @validator('username')
    def validate_username(cls, v):
        # Length already handled by Field
        
        # Only letters, numbers, underscore
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Username can only contain letters, numbers, and underscore')
        
        # No consecutive underscores
        if '__' in v:
            raise ValueError('Username cannot have consecutive underscores')
        
        # No start/end with underscore
        if v.startswith('_') or v.endswith('_'):
            raise ValueError('Username cannot start or end with underscore')
        
        return v
    
    # ===== PASSWORD VALIDATION =====
    @validator('password')
    def validate_password(cls, v):
        # Minimum length
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        
        # Maximum length (bcrypt limit)
        if len(v) > 72:
            raise ValueError('Password cannot exceed 72 characters')
        
        # Contains uppercase
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain at least one uppercase letter')
        
        # Contains lowercase
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain at least one lowercase letter')
        
        # Contains number
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
    
    class Config:
        from_attributes = True

# ========== PASSWORD HASHING ==========
def simple_hash(password: str):
    """Simple hash using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

# ========== ENDPOINTS ==========
@app.get("/")
def root():
    return {
        "message": "Server working!",
        "status": "success",
        "version": "1.0.0",
        "features": [
            "Email validation (15 rules)",
            "Username validation (3-20 chars, alphanumeric + _)",
            "Password validation (8-72 chars, upper, lower, number)",
            "Case-insensitive email checking"
        ]
    }

@app.get("/test")
def test(db: Session = Depends(database.get_db)):
    try:
        db.execute("SELECT 1").first()
        return {"success": True, "database": "connected"}
    except Exception as e:
        return {"success": False, "database": "error", "details": str(e)}

@app.post("/register", response_model=UserResponse, status_code=201)
def register(user: UserCreate, db: Session = Depends(database.get_db)):
    try:
        # CASE-INSENSITIVE EMAIL CHECK (CRITICAL FIX!)
        existing_email = db.query(models.User).filter(
            func.lower(models.User.email) == func.lower(user.email)
        ).first()
        
        if existing_email:
            raise HTTPException(400, "Email already registered")
        
        # Username check (case-sensitive - usernames are case-sensitive)
        existing_username = db.query(models.User).filter(
            models.User.username == user.username
        ).first()
        
        if existing_username:
            raise HTTPException(400, "Username already taken")
        
        # Hash password
        hashed_password = simple_hash(user.password)
        
        # Create user (email already lowercased by validator)
        db_user = models.User(
            email=user.email,  # Already lowercase from validator
            username=user.username,
            full_name=user.full_name,
            hashed_password=hashed_password,
            role="customer",
            is_active=True
        )
        
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in registration: {e}")
        raise HTTPException(500, f"Internal server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("="*60)
    print("🚀 AUTORESOLVE AI - PHASE 3 PRODUCTION")
    print("="*60)
    print("✅ Email: 15 validation rules + case-insensitive")
    print("✅ Username: 3-20 chars, alphanumeric + underscore")
    print("✅ Password: 8-72 chars, upper, lower, number")
    print("✅ Case-insensitive email checking (FIXED!)")
    print("="*60)
    print("🌐 http://localhost:8001")
    print("📚 http://localhost:8001/docs")
    print("="*60)
    uvicorn.run(app, host="0.0.0.0", port=8001)