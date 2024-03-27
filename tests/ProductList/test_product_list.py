import json
from pydantic import ValidationError
import pytest
from api.main import ProductList, User
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


@pytest.mark.parametrize(['name',
                          'price',
                          'category',
                          'stock',
                          'availability',
                          'expected_result'],
                          [
                              (50*'a', 5.55, 20*'c', 500, True, True),
                              ('', '' , None, '', False, False),
                              (3*'a', 5, None, 'd', False, False),
                              (1, None, 3, None, None, False),
                          ])
def test_product_list_base_model(name, price, category, stock, availability, expected_result):
    if expected_result:
        products = ProductList(name=name, price=price, product_category=category, stock=stock, availability=availability)
        assert products.name == name
        assert products.price == price
        assert products.product_category == category
        assert products.stock == stock
        assert products.availability == availability
    else:
        with pytest.raises(ValidationError):
            products = ProductList(name=name, price=price, product_category=category, stock=stock, availability=availability)


#@fast_app.get("/product/")
def test_no_products(api_client):
    response = api_client.get("/product/")
    assert response.status_code == 200
    print(response.json())
    assert response.json() == Messages.NO_ITEMS_FOUND


#@fast_app.post("/product/")
def test_add_valid_product_list(api_client, valid_single_product_item_list: dict):
    response = api_client.post("/product/", json=valid_single_product_item_list)
    assert response.status_code == 200
    assert response.json() == valid_single_product_item_list
        

#@fast_app.post("/product/")
def test_add_invalid_product_list(api_client, invalid_product_item_list: dict[str, any]):
    response = api_client.post("/product/", json=invalid_product_item_list)
    assert response.status_code == 422


#@fast_app.get("/product/")
def test_get_all_products(api_client,valid_second_product_item_list: dict ):
    post_response = api_client.post("/product/", json=valid_second_product_item_list)
    get_response = api_client.get("/product/")
    print(get_response.json())
    assert get_response.status_code == 200
    assert len(get_response.json()) == 2


#@fast_app.get("/product/{product_id}")
def test_get_single_product(api_client, valid_second_product_item_list):
    product_id = 1
    response = api_client.get(f"/product/{product_id}")
    print(response.json())
    assert response.status_code == 200
    assert response.json() == valid_second_product_item_list


#@fast_app.get("/product/{product_id}")
def test_get_single_product_not_found(api_client):
    product_id = 2
    response = api_client.get(f"/product/{product_id}")
    print(response.json())
    assert response.status_code == 200
    assert response.json()['message'] == Messages.NOT_FOUND



