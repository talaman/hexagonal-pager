from fastapi.testclient import TestClient
from pager.adapters.fastapi_adapter import app

client = TestClient(app)

def test_receive_alert():
    response = client.post("/alert", json={"service_id": "service1", "message": "Test Alert"})
    assert response.status_code == 200
    assert response.json() == {"status": "Alert received"}

def test_acknowledge_alert():
    response = client.post("/acknowledge", json={"service_id": "service1"})
    assert response.status_code == 200
    assert response.json() == {"status": "Acknowledgement received"}

def test_healthy_event():
    response = client.post("/healthy", json={"service_id": "service1"})
    assert response.status_code == 200
    assert response.json() == {"status": "Healthy event received"}