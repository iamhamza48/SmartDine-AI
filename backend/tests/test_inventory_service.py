from unittest.mock import patch
from app.services.inventory_service import get_low_stock_items

@patch("app.services.inventory_service.get_all_inventory")
def test_low_stock_filters_correctly(mock_get_all):
    mock_get_all.return_value = [
        {"item_name": "Chicken", "quantity": 12, "unit": "kg", "minimum_level": 15},
        {"item_name": "Rice", "quantity": 30, "unit": "kg", "minimum_level": 10},
    ]
    result = get_low_stock_items("any-id")
    assert len(result) == 1
    assert result[0]["item_name"] == "Chicken"