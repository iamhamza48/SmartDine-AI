from langchain_core.tools import tool
from app.services.forecast_service import predict_demand

@tool
def forecast_demand(date: str) -> float:
    """Predicts item demand for a given date (YYYY-MM-DD) using the trained ML model."""
    return predict_demand(date)