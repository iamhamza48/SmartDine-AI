from langchain_core.tools import tool
from app.services.analytics_service import get_revenue, compare_periods

@tool
def revenue_for_period(restaurant_id: str, start: str, end: str) -> float:
    """Returns total revenue for a restaurant between two dates (YYYY-MM-DD)."""
    return get_revenue(restaurant_id, start, end)

@tool
def compare_revenue_periods(restaurant_id: str, start_a: str, end_a: str, start_b: str, end_b: str) -> dict:
    """Compares total revenue between two date ranges."""
    return compare_periods(restaurant_id, start_a, end_a, start_b, end_b)