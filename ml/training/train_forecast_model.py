import pandas as pd
import joblib
from sklearn.ensemble import HistGradientBoostingRegressor
from backend.app.config.db import engine

df = pd.read_sql("""
    select s.quantity, s.sale_date, m.name as menu_item
    from sales s join menu_items m on s.menu_item_id = m.id
""", engine)

df["sale_date"] = pd.to_datetime(df["sale_date"])
df["day_of_week"] = df["sale_date"].dt.dayofweek
df["month"] = df["sale_date"].dt.month

X = df[["day_of_week", "month"]]
y = df["quantity"]

# baseline first, always compare against it
baseline_mae = (y - y.mean()).abs().mean()
print(f"Baseline (mean) MAE: {baseline_mae:.2f}")

model = HistGradientBoostingRegressor().fit(X, y)
joblib.dump(model, "ml/models/forecast_model.pkl")
print("Model saved.")