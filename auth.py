from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'])

def hash_password(password: str) -> str:
  hashed = pwd_context.hash(password)
  print(f"plain: {password}, hashed: {hashed}")
  return hashed