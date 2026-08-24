import os, uuid, random
from datetime import date, timedelta
import psycopg2
from dotenv import load_dotenv

load_dotenv("backend/.env")

conn = psycopg2.connect(os.environ["DATABASE_URL"])
cur = conn.cursor()

# --- restaurant (reuse if it already exists) ---
cur.execute("select id from restaurants limit 1")
row = cur.fetchone()
if row:
    restaurant_id = row[0]
else:
    restaurant_id = str(uuid.uuid4())
    cur.execute("insert into restaurants (id, name) values (%s, %s)", (restaurant_id, "Demo Bistro"))

# --- inventory (skip if already seeded) ---
cur.execute("select count(*) from inventory where restaurant_id=%s", (restaurant_id,))
if cur.fetchone()[0] == 0:
    items = [("Chicken", "kg", 12, 15), ("Rice", "kg", 30, 10), ("Tomatoes", "kg", 3, 8)]
    for name, unit, qty, minimum in items:
        cur.execute(
            "insert into inventory (restaurant_id, item_name, quantity, unit, minimum_level) values (%s,%s,%s,%s,%s)",
            (restaurant_id, name, qty, unit, minimum)
        )

# --- menu items ---
cur.execute("select id, name from menu_items where restaurant_id=%s", (restaurant_id,))
menu_items = cur.fetchall()
if not menu_items:
    menu_data = [("Grilled Chicken", "mains", 12.99), ("Chicken Rice Bowl", "mains", 9.99), ("Veg Curry", "mains", 8.50)]
    menu_items = []
    for name, category, price in menu_data:
        item_id = str(uuid.uuid4())
        cur.execute(
            "insert into menu_items (id, restaurant_id, name, category, price) values (%s,%s,%s,%s,%s)",
            (item_id, restaurant_id, name, category, price)
        )
        menu_items.append((item_id, name))

# --- 90 days of sales, weekday/weekend pattern baked in ---
cur.execute("select count(*) from sales where restaurant_id=%s", (restaurant_id,))
if cur.fetchone()[0] == 0:
    start = date.today() - timedelta(days=90)
    for day_offset in range(90):
        d = start + timedelta(days=day_offset)
        is_weekend = d.weekday() >= 5
        for item_id, name in menu_items:
            base = 15 if is_weekend else 8
            qty = max(0, int(random.gauss(base, 3)))
            price = 10.0
            cur.execute(
                "insert into sales (restaurant_id, menu_item_id, quantity, sale_date, revenue) values (%s,%s,%s,%s,%s)",
                (restaurant_id, item_id, qty, d.isoformat(), qty * price)
            )

conn.commit()
print("Seeded restaurant:", restaurant_id)
print("Menu items:", len(menu_items))
cur.execute("select count(*) from sales where restaurant_id=%s", (restaurant_id,))
print("Sales rows:", cur.fetchone()[0])