import sys
import os

# Add the root directory of your project to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi.testclient import TestClient
from api.main import app
import pytest


@pytest.fixture()
def api_client():
    return TestClient(app)



@pytest.fixture()
def valid_product_item_list():
    return {
        "name": "Item 1",
        "price": 55.00,
        "product_category": "QA",
        "stock": 0,
        "availability": False,
        }
        
@pytest.fixture()
def invalid_product_item_list():
    return [{
        "name": "Item 1",
        "price": 55.00,
        "product_category": "QA",
        "stock": 0,
        "availability": False,
        },]