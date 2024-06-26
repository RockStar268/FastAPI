import sys
import os

# Add the root directory of your project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi.testclient import TestClient
from api.main import fast_app
import pytest


@pytest.fixture()
def api_client():
    return TestClient(fast_app)



@pytest.fixture()
def valid_single_product_item_list():
    product = {
        "name": "Item 1",
        "price": 55.00,
        "product_category": "QA",
        "stock": 0,
        "availability": False,
        }
    return product


@pytest.fixture()
def valid_second_product_item_list():
    product = {
        "name": "Item 2",
        "price": 5.00,
        "product_category": "Engineer",
        "stock": 500,
        "availability": True,
        }
    return product


@pytest.fixture()
def valid_updated_product_item_list():
    product = {
        "name": "Updated Item",
        "price": 5.00,
        "product_category": "Engineer",
        "stock": 500,
        "availability": True,
        }
    return product


@pytest.fixture()
def invalid_updated_product_item_list():
    product = {
        "name": "Invalid Item",
        "price": "Invalid Price",
        "product_category": "Engineer",
        "stock": 500,
        "availability": True,
        }
    return product


@pytest.fixture()
def invalid_product_item_list():
    return {
        "name": "Item 1",
        "price": "fifty five",
        "product_category": "QA",
        "stock": 0,
        "availability": False,
        }

@pytest.fixture()
def valid_user():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "John@Doe.com",
        "password": "JonhDoe123"
    }

@pytest.fixture()
def invalid_user():
    return {
        "first_name": "John",
        "last_name": "Doe",
        "email": "@Doe.com",
        "password": "JonhDoe123"
    }


@pytest.fixture()
def update_with_valid_user():
    return {
        "first_name": "Updated",
        "last_name": "Valid User",
        "email": "Updated@Doe.com",
        "password": "JonhDoe123"
    }

@pytest.fixture()
def update_with_invalid_user():
    return {
        "first_name": "Updated",
        "last_name": "Valid User",
        "email": "Updated@Doe.",
        "password": "JonhDoe123"
    }