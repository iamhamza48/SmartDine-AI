from fastapi import APIRouter

from app.services.inventory_service import get_low_stock_items
router = APIRouter()



@router.get("/inventory")
def list_inventory():
    # TODO Phase 1: replace with repository call
    return [{"item_name": "Chicken", "quantity": 12, "minimum_level": 15}]



@router.get("/inventory/low-stock")
def low_stock(restaurant_id: str):
    return get_low_stock_items(restaurant_id)

    
