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
def valid_second_product_item_list():
    products = {
        "name": "Item 2",
        "price": 5.00,
        "product_category": "Engineer",
        "stock": 500,
        "availability": True,
        }
    return products

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
def invalid_product_item_list():
    return {
        "name": "Item 1",
        "price": "fifty five",
        "product_category": "QA",
        "stock": 0,
        "availability": False,
        }

