from sqlalchemy import text
from app.config.db import engine

def get_all_inventory(restaurant_id: str) -> list[dict]:
    with engine.connect() as conn:
        rows = conn.execute(
            text("""
                select item_name, quantity, unit, minimum_level
                from inventory
                where restaurant_id = :rid
            """),
            {"rid": restaurant_id}
        ).fetchall()
    return [dict(r._mapping) for r in rows]