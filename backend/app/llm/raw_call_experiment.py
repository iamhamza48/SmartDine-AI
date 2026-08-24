from pydantic import BaseModel
from google.genai import types
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from google.genai.errors import ClientError
from app.llm.gemini_client import client, MODEL

class RestockRecommendation(BaseModel):
    item_name: str
    recommended_quantity: float
    unit: str
    reason: str

@retry(
    stop=stop_after_attempt(4),
    wait=wait_exponential(multiplier=2, min=2, max=30),
    retry=retry_if_exception_type(ClientError),
)
def get_restock_recommendation(inventory_text: str) -> RestockRecommendation:
    response = client.models.generate_content(
        model=MODEL,
        contents=f"Given this inventory, recommend a restock:\n{inventory_text}",
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=RestockRecommendation,   # native structured output — no manual JSON parsing
            temperature=0.2,
        ),
    )
    return RestockRecommendation.model_validate_json(response.text)

if __name__ == "__main__":
    result = get_restock_recommendation("Chicken: 12kg (minimum 15kg). Rice: 30kg (minimum 10kg).")
    print(result)