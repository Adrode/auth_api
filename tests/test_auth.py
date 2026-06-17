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