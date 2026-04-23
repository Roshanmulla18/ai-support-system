"""
Fix test user passwords by rehashing with bcrypt
"""
from database import SessionLocal
from models import User
import auth

db = SessionLocal()

# Test user passwords
test_users = [
    ("testuser", "Test@1234"),
    ("roshanmulla", "Roshan@123"),
    ("rosha", "Rosha@123"),
    ("string", "String@123"),
    ("janesmith", "Jane@1234"),
]

print("\n🔄 Rehashing test user passwords with bcrypt...\n")

for username, password in test_users:
    user = db.query(User).filter(User.username == username).first()
    if user:
        hashed = auth.get_password_hash(password)
        user.hashed_password = hashed
        db.commit()
        print(f"✅ {username}: {hashed[:30]}... (length: {len(hashed)})")
    else:
        print(f"❌ {username}: User not found")

print("\n✅ All test user passwords updated with bcrypt hashing!\n")
