from langchain_core.tools import tool
from app.services.inventory_service import get_low_stock_items

@tool
def check_low_stock(restaurant_id: str) -> list[dict]:
    """Returns inventory items that are below their minimum stock level for a given restaurant."""
    return get_low_stock_items(restaurant_id)