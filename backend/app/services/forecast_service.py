import joblib
import pandas as pd
from functools import lru_cache
from pathlib import Path


# Project root:
# AiRestaurantManager/
# ├── backend/
# └── ml/
PROJECT_ROOT = Path(__file__).resolve().parents[3]

MODEL_PATH = PROJECT_ROOT / "ml" / "models" / "forecast_model.pkl"


@lru_cache
def _load_model():
    return joblib.load(MODEL_PATH)


def predict_demand(date: str) -> float:
    model = _load_model()

    dt = pd.to_datetime(date)

    features = pd.DataFrame([
        {
            "day_of_week": dt.dayofweek,
            "month": dt.month
        }
    ])

    return float(model.predict(features)[0])