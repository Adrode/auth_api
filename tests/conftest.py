import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, StaticPool, delete
from sqlalchemy.orm import sessionmaker
from main import app
from database.database import get_db
from database.models import Base, User
from authentication.short import hash_password

engine = create_engine(
  "sqlite:///:memory:",
  connect_args={"check_same_thread": False},
  poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
  session = TestingSessionLocal()
  try:
    yield session
  finally:
    session.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def setup_db():
  Base.metadata.create_all(bind=engine)
  yield
  Base.metadata.drop_all(bind=engine)

@pytest.fixture()
def db_session():
  session = TestingSessionLocal()
  try:
    yield session
  finally:
    session.close()

@pytest.fixture()
def client():
  return TestClient(app)

@pytest.fixture(autouse=True)
def clean_db(db_session):
  yield
  db_session.execute(delete(User))
  db_session.commit()

@pytest.fixture()
def test_first_user(db_session):
  password = "kekw"

  user = User(
    email="adrianwozniak20@gmail.com",
    hashed_password=hash_password(password)
  )

  db_session.add(user)
  db_session.commit()
  db_session.refresh(user)

  user.plain_password = password

  return user

@pytest.fixture()
def token_first_user(client, test_first_user):
  response = client.post(
    "/auth/login",
    data={
      "username": test_first_user.email,
      "password": test_first_user.plain_password
    }
  )

  token = response.json()["access_token"]

  return token

@pytest.fixture()
def authenticate_first_user(token_first_user):
  return {"Authorization": f"Bearer {token_first_user}"}