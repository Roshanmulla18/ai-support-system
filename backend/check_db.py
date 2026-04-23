from database import SessionLocal
from models import User

db = SessionLocal()
users = db.query(User).all()

print(f"\n{'Username':<20} {'Email':<25} {'Hash (first 30 chars)':<30} {'Hash Length':<15}")
print("=" * 90)

for user in users[:5]:
    hash_preview = user.hashed_password[:30] if user.hashed_password else "None"
    hash_length = len(user.hashed_password) if user.hashed_password else 0
    print(f"{user.username:<20} {user.email:<25} {hash_preview:<30} {hash_length:<15}")
