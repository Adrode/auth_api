from dotenv import load_dotenv
import os, hashlib, secrets
from datetime import datetime, timedelta, timezone

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
DAYS_TO_EXPIRE = 7

def create_refresh_token(): # refresh token może być losowym stringiem, nie musi być JWT
  token = secrets.token_urlsafe(64)
  hashed_token = hashlib.sha256(token.encode()).hexdigest()
  expires_at = datetime.now(timezone.utc) + timedelta(days=DAYS_TO_EXPIRE)
  return token, hashed_token, expires_at