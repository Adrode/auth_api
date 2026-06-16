def test_get_me_valid_data(client, authenticate_first_user):
  response = client.get(
    "/users/me",
    headers=authenticate_first_user
  )

  assert response.status_code == 200