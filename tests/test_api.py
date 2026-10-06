from fastapi.testclient import TestClient
from backend.main import app, state

client = TestClient(app)

def test_new_test_starts_at_zero():
    state["measurements"] = []
    r = client.post("/api/test/start", json={"operator": "B"})
    assert r.status_code == 200
    assert r.json()["record_index"] == 0

def test_measurement_keeps_raw_value():
    client.post("/api/test/start", json={"operator": "B"})
    r = client.post("/api/measurement", json={
        "parameter": "thrust",
        "raw_value": 1.65,
        "unit": "kgf",
        "source": "LIVE_SENSOR"
    })
    assert r.json()["raw_value"] == 1.65
    assert "corrected_value" in r.json()

def test_stop_stops_measurements():
    client.post("/api/test/stop")
    r = client.post("/api/measurement", json={
        "parameter": "thrust",
        "raw_value": 1.65,
        "source": "LIVE_SENSOR"
    })
    assert r.json()["status"] == "REJECTED"
