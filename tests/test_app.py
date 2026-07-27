import copy

from fastapi.testclient import TestClient

from src import app as app_module
from src.app import app


ORIGINAL_ACTIVITIES = copy.deepcopy(app_module.activities)
client = TestClient(app)


def _reset_activities():
    app_module.activities = copy.deepcopy(ORIGINAL_ACTIVITIES)


def setup_function():
    _reset_activities()


def teardown_function():
    _reset_activities()


def test_signup_for_activity_adds_new_participant():
    # Arrange
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"

    activities_response = client.get("/activities")
    activity = activities_response.json()["Chess Club"]
    assert email in activity["participants"]


def test_signup_for_activity_returns_400_for_duplicate_email():
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already registered for this activity"


def test_unregister_participant_removes_email_from_activity():
    # Arrange
    email = "michael@mergington.edu"

    # Act
    response = client.delete(f"/activities/Chess%20Club/participants/{email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from Chess Club"

    activities_response = client.get("/activities")
    activity = activities_response.json()["Chess Club"]
    assert email not in activity["participants"]


def test_unregister_participant_returns_404_for_missing_activity():
    # Arrange
    email = "student@example.com"

    # Act
    response = client.delete(f"/activities/Does%20Not%20Exist/participants/{email}")

    # Assert
    assert response.status_code == 404
