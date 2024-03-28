import json
from pydantic import ValidationError
import pytest
from api.main import  User
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
        user = User(first_name=first_name,
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
            user = User(first_name=first_name,
                last_name=last_name,
                email=email,
                password=password
                )


#@fast_app.get("/users/")
def test_get_all_users(api_client):
    response = api_client.get("/users/")
    assert response.status_code == 200
    assert response.json()['message'] == Messages.NO_USERS_FOUND


#@fast_app.get("/users/")
def test_add_valid_user(api_client, valid_user):
    response = api_client.post("/users/", json=valid_user)
    assert response.status_code == 200
    assert response.json() == valid_user


#@fast_app.get("/users/")
def test_add_invalid_user(api_client, invalid_user):
    response = api_client.post("/users/", json=invalid_user)
    assert response.status_code == 422
