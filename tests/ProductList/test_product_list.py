import json
from pydantic import ValidationError
import pytest
from api.main import ProductList
from enums.Messages import Messages



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
    assert response.status_code == 404
    assert response.json()['detail'] == Messages.NO_ITEMS_FOUND


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
    assert get_response.status_code == 200
    assert len(get_response.json()) == 2


#@fast_app.get("/product/{product_id}")
def test_get_single_product(api_client, valid_second_product_item_list):
    product_id = 1
    response = api_client.get(f"/product/{product_id}")
    assert response.status_code == 200
    assert response.json() == valid_second_product_item_list


#@fast_app.get("/product/{product_id}")
def test_get_single_product_not_found(api_client):
    product_id = 2
    response = api_client.get(f"/product/{product_id}")
    assert response.status_code == 404
    assert response.json()['detail'] == Messages.ITEM_NOT_FOUND


#@fast_app.put("/product/{product_id}/update/")
def test_update_existing_item(api_client, valid_updated_product_item_list):
    product_id = 1
    response = api_client.put(f"/product/{product_id}/update", json=valid_updated_product_item_list)
    assert response.status_code == 200
    assert response.json() == valid_updated_product_item_list


#@fast_app.put("/product/{product_id}/update/")
def test_update_non_existing_item__with_valid_item(api_client, valid_updated_product_item_list):
    product_id = 10
    response = api_client.put(f"/product/{product_id}/update", json=valid_updated_product_item_list)
    assert response.status_code == 404
    assert response.json()['detail'] == Messages.ITEM_NOT_FOUND


#@fast_app.put("/product/{product_id}/update/")
def test_update_existing_item_with_invalid_item(api_client, invalid_updated_product_item_list):
    product_id = 0
    response = api_client.put(f"/product/{product_id}/update", json=invalid_updated_product_item_list)
    assert response.status_code == 422
    

#@fast_app.delete("/product/{product_id}/delete/")
def test_delete_existing_item(api_client):
    product_id = 1
    response = api_client.delete(f"/product/{product_id}/delete/")
    assert response.status_code == 200
    assert response.json()['message'] == Messages.ITEM_DELETED


#@fast_app.delete("/product/{product_id}/delete/")
def test_delete_non_existing_item(api_client):
    product_id = 50
    response = api_client.delete(f"/product/{product_id}/delete/")
    assert response.status_code == 404
    assert response.json()['detail'] == Messages.ITEM_NOT_FOUND
