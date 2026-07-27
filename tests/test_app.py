from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    response = client.delete(
        "/activities/Chess%20Club/participants/michael@mergington.edu"
    )

    assert response.status_code == 200
    assert "michael@mergington.edu" in response.json()["message"]

    activities_response = client.get("/activities")
    activity = activities_response.json()["Chess Club"]
    assert "michael@mergington.edu" not in activity["participants"]


def test_unregister_participant_returns_404_for_missing_activity():
    response = client.delete(
        "/activities/Does%20Not%20Exist/participants/student@example.com"
    )

    assert response.status_code == 404
