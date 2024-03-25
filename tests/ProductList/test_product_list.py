import json

from enums.Messages import Messages

#@fast_app.get("/product/")
def test_no_products(api_client):
    response = api_client.get("/product/")
    assert response.status_code == 200
    print(response.json())
    assert response.json() == []


#@fast_app.post("/product/")
def test_add_valid_product_list(api_client, valid_single_product_item_list: dict):
    response = api_client.post("/product/", json=valid_single_product_item_list)
    assert response.status_code == 200
    assert response.json()[0] == valid_single_product_item_list
        

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