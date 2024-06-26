import json
from pydantic import ValidationError
import pytest
from api.main import BaseUser, CreateUser
from enums.Messages import Messages


@pytest.mark.parametrize(['first_name', 
                          'last_name',
                          'email',
                          'password',
                          'expected_results'],
                          [
                              ('John', 'Doe', 'test@test.com', 'John_Doe', True),
                              (51*'a', 51*'b', 41*'c'+'@'+5*'d'+'.com', 51*'e', False),
                              (50*'a', 50*'b', 40*'c'+'@'+5*'d'+'.com', 50*'e', True),
                              ('', 3*'b', 'c@d.com', 8*'e', True),
                              ('John', 'Do', '', 'IamTesting', False),
                              ('John', 'Doe', '@test.com', 'IamTesting', False),
                              ('John', 'Doe', 'John@', 'IamTesting', False),
                              ('John', 'Doe', 'John@doe', 'IamTesting', False),
                              ('John', 'Doe', 'John@.com', 'IamTesting', False),
                              ('John', 'Doe', 'John@doe.', 'IamTesting', False),
                              (1, 2, 3, 4, False),
                          ])
def test_user_base_model(first_name, last_name, email, password, expected_results):
    if expected_results:
        user = CreateUser(first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
                )
        assert user.first_name == first_name
        assert user.last_name == last_name
        assert user.email == email
        assert user.password == password
    else: 
        with pytest.raises(ValidationError):
            user = CreateUser(first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
                )


#@fast_app.get("/users/")
def test_get_all_users(api_client):
    response = api_client.get("/users/")
    assert response.status_code == 404
    assert response.json()['detail'] == Messages.NO_USERS_FOUND


#@fast_app.post("/users/")
def test_add_valid_user(api_client, valid_user):
    response = api_client.post("/users/", json=valid_user)
    assert response.status_code == 200
    assert response.json()['first_name'] == valid_user['first_name']
    assert response.json()['last_name'] == valid_user['last_name']
    assert response.json()['email'] == valid_user['email']
    assert valid_user['password'] not in response.json()


#@fast_app.post("/users/")
def test_add_invalid_user(api_client, invalid_user):
    response = api_client.post("/users/", json=invalid_user)
    assert response.status_code == 422



#@fast_app.get("/users/{user_id}")
def test_get_existing_user(api_client):
    user_id = 0
    response = api_client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert 'first_name' in response.json()
    assert 'last_name' in response.json()
    assert 'email' in response.json()
    assert 'password' not in response.json()


#@fast_app.get("/users/{user_id}")
def test_get_non_existing_user(api_client):
    user_id = 10
    response = api_client.get(f"/users/{user_id}")
    assert response.status_code == 404
    assert response.json()['detail'] == Messages.USER_NOT_FOUND


#@fast_app.put("/users/{user_id}/update")
def test_update_existing_user(api_client, update_with_valid_user):
    user_id = 0
    response = api_client.put(f"/users/{user_id}/update", json=update_with_valid_user)
    assert response.status_code == 200
    assert response.json()['first_name'] == update_with_valid_user['first_name']
    assert response.json()['last_name'] == update_with_valid_user['last_name']
    assert response.json()['email'] == update_with_valid_user['email']
    assert update_with_valid_user['password'] not in response.json()



#@fast_app.put("/users/{user_id}/update")
def test_update_non_existing_user_with_valid_user(api_client, update_with_valid_user):
    user_id = 10
    response = api_client.put(f"/users/{user_id}/update", json=update_with_valid_user)
    assert response.status_code == 404
    assert response.json()['detail'] == Messages.USER_NOT_FOUND


#@fast_app.put("/users/{user_id}/update")
def test_update_existing_user_with_invalid_user(api_client, update_with_invalid_user):
    user_id = 0
    response = api_client.put(f"/users/{user_id}/update", json=update_with_invalid_user)
    assert response.status_code == 422


#@fast_app.delete("/users/{user_id}/delete")
def test_delete_existing_user(api_client):
    user_id = 0
    response = api_client.delete(f"/users/{user_id}/delete")
    assert response.status_code == 200
    assert response.json()['message'] == Messages.USER_DELETED

#@fast_app.delete("/users/{user_id}/delete")
def test_delete_non_existing_user(api_client):
    user_id = 10
    response = api_client.delete(f"/users/{user_id}/delete")
    assert response.status_code == 404
    assert response.json()['detail'] == Messages.USER_NOT_FOUND

