from sqlalchemy import select, func
from database import models
from authentication.short import hash_password

def test_register_valid_data(client):
  response = client.post(
    "/auth/register",
    json={
      "email": "adrian@gmail.com",
      "password": hash_password("kekw")
    }
  )

  assert response.status_code == 200
  assert response.json()["email"] == "adrian@gmail.com"

def test_register_invalid_data(client):
  response = client.post(
    "/auth/register",
    json={
      "email": "alabama",
      "password": "mama"
    }
  )
  
  assert response.status_code == 422

def test_register_email_not_unique(client, test_first_user):
  response = client.post(
    "/auth/register",
    json={
      "email": test_first_user.email,
      "password": hash_password("foo")
    }
  )

  assert response.status_code == 400

def test_login_valid_data(client, test_first_user):
  response = client.post(
    "/auth/login",
    data={
      "username": test_first_user.email,
      "password": test_first_user.plain_password
    }
  )

  assert response.status_code == 200
  assert "access_token" and "refresh_token" in response.json()

def test_login_invalid_user(client):
  response = client.post(
    "/auth/login",
    data={
      "username": "kekw@gmail.com",
      "password": 123
    }
  )

  assert response.status_code == 401

def test_login_5_refresh_tokens(client, test_first_user, db_session):
  i = 6
  while i > 0:
    client.post(
      "/auth/login",
      data={
        "username": test_first_user.email,
        "password": test_first_user.plain_password
      }
    )
    i -= 1

  response = client.post(
      "/auth/login",
      data={
        "username": test_first_user.email,
        "password": test_first_user.plain_password
      }
    )

  count_refresh_tokens = db_session.scalar(
    select(func.count(models.RefreshToken.id)).where(models.RefreshToken.user_id == test_first_user.id)
  )

  assert response.status_code == 200
  assert count_refresh_tokens <= 5

def test_refresh_valid_data(client, test_first_user):
  login = client.post(
    "/auth/login",
    data={
      "username": test_first_user.email,
      "password": test_first_user.plain_password
    }
  )

  response = client.post(
    "/auth/refresh",
    json={
      "refresh_token": login.json()["refresh_token"]
    }
  )

  assert response.status_code == 200
  assert response.json()["refresh_token"] != login.json()["refresh_token"]

def test_refresh_invalid_old_token(client):
  response = client.post(
    "/auth/refresh",
    json={
      "refresh_token": "kekw"
    }
  )

  assert response.status_code == 401

def test_refresh_user_agent_mismatch(client, test_first_user):
  login = client.post(
    "/auth/login",
    headers={
      "User-Agent": "MyUserAgentKEKW",
    },
    data={
      "username": test_first_user.email,
      "password": test_first_user.plain_password
    }
  )

  response = client.post(
    "/auth/refresh",
    json={
      "refresh_token": login.json()["refresh_token"]
    }
  )

  assert response.status_code == 200
  assert response.json()["warnings"]["user-agent"] == "Suspicious device"

def test_logout_valid_data(client, test_first_user):
  login = client.post(
    "/auth/login",
    data={
      "username": test_first_user.email,
      "password": test_first_user.plain_password
    }
  )

  response = client.post(
    "/auth/logout",
    json={
      "refresh_token": login.json()["refresh_token"]
    }
  )

  assert response.status_code == 200
  assert response.json()["detail"] == "Logged out"

def test_logout_invalid_old_token(client):
  response = client.post(
    "/auth/logout",
    json={
      "refresh_token": "kekw"
    }
  )

  assert response.status_code == 401