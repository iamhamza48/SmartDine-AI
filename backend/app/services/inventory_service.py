from app.repositories.inventory_repository import get_all_inventory

def get_low_stock_items(restaurant_id: str) -> list[dict]:
    items = get_all_inventory(restaurant_id)
    return [i for i in items if float(i["quantity"]) < float(i["minimum_level"])]