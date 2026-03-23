from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'])

print("schemes: ", pwd_context.schemes())
print("default scheme: ", pwd_context.default_scheme())

def hash_password(password: str) -> str:
  hashed = pwd_context.hash(password)
  print(f"plain: {password}, hashed: {hashed}")
  return hashed