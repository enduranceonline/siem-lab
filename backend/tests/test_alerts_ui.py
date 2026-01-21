from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_alerts_status_invalid_returns_422():
    r = client.get("/alerts", params={"status": "banana"})
    assert r.status_code == 422


def test_alerts_ui_severity_range_invalid_returns_422():
    r = client.get("/alerts/ui", params={"severity_min": 9, "severity_max": 3})
    assert r.status_code == 422


def test_alerts_ui_count_returns_int():
    r = client.get("/alerts/ui/count", params={"severity_min": 0})
    assert r.status_code == 200
    # FastAPI response_model=int -> JSON number
    assert isinstance(r.json(), int)
    assert r.json() >= 0
