from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_list_inventory_returns_200():
    r = client.get("/api/inventory")

    assert r.status_code == 200
    assert isinstance(r.json(), list)