from sqlalchemy import text
from app.config.db import engine

def get_revenue(restaurant_id: str, start: str, end: str) -> float:
    with engine.connect() as conn:
        result = conn.execute(
            text("""
                select coalesce(sum(revenue), 0) from sales
                where restaurant_id = :rid and sale_date between :start and :end
            """),
            {"rid": restaurant_id, "start": start, "end": end}
        ).scalar()
    return float(result)

def compare_periods(restaurant_id: str, start_a: str, end_a: str, start_b: str, end_b: str) -> dict:
    return {
        "period_a_revenue": get_revenue(restaurant_id, start_a, end_a),
        "period_b_revenue": get_revenue(restaurant_id, start_b, end_b),
    }