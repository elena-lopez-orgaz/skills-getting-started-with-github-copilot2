from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"]["participants"], list)

def test_signup():
    response = client.post("/activities/Chess Club/signup?email=test@example.com")
    assert response.status_code == 200
    # Verify added
    response = client.get("/activities")
    data = response.json()
    assert "test@example.com" in data["Chess Club"]["participants"]

def test_signup_duplicate():
    # First signup
    client.post("/activities/Chess Club/signup?email=duplicate@example.com")
    # Second
    response = client.post("/activities/Chess Club/signup?email=duplicate@example.com")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

def test_remove():
    # Signup first
    client.post("/activities/Chess Club/signup?email=remove@example.com")
    # Remove
    response = client.delete("/activities/Chess Club/remove?email=remove@example.com")
    assert response.status_code == 200
    # Verify removed
    response = client.get("/activities")
    data = response.json()
    assert "remove@example.com" not in data["Chess Club"]["participants"]

def test_remove_not_signed():
    response = client.delete("/activities/Chess Club/remove?email=notsigned@example.com")
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]

def test_activity_not_found():
    response = client.post("/activities/Nonexistent/signup?email=test@example.com")
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]

def test_root_redirect():
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"