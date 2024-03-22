import json


def test_add_valid_product_list(api_client, valid_product_item_list: dict[str, any]):
    response = api_client.post("/item/", json=valid_product_item_list)
    assert response.status_code == 200
    for item in response.json():
        assert item == valid_product_item_list

def test_add_invalid_product_list(api_client, invalid_product_item_list: dict[str, any]):
    response = api_client.post("/item/", json=invalid_product_item_list)
    assert response.status_code == 422

