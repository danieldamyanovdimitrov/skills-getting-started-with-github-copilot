from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture(autouse=True)
def reset_activities():
    original = deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)


@pytest.fixture
def client():
    return TestClient(app)


def test_get_activities_includes_added_examples(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert len(response.json()) >= 4


def test_signup_rejects_duplicate_participant(client):
    activity = "Chess Club"
    existing_participant = "michael@mergington.edu"

    response = client.post(f"/activities/{activity}/signup?email={existing_participant}")

    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"


def test_unregister_participant_removes_student(client):
    activity = "Chess Club"
    participant = "michael@mergington.edu"

    response = client.delete(f"/activities/{activity}/participants/{participant}")

    assert response.status_code == 200
    assert participant not in activities[activity]["participants"]
