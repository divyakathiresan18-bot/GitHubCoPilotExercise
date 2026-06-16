"""
Tests for the Mergington High School API using TestClient and AAA pattern.

Arrange-Act-Assert style tests that reset the in-memory `activities`
before each test for isolation.
"""

import copy
import urllib.parse
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    initial_state = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Soccer Team": {
            "description": "Practice teamwork and compete in intramural soccer matches",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 18,
            "participants": ["ella@mergington.edu", "liam@mergington.edu"]
        },
        "Swimming Club": {
            "description": "Build swimming skills and prepare for swim meets",
            "schedule": "Mondays and Wednesdays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["grace@mergington.edu", "noah@mergington.edu"]
        },
        "Art Workshop": {
            "description": "Explore painting, drawing, and mixed media projects",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["mia@mergington.edu", "lucas@mergington.edu"]
        },
        "Drama Club": {
            "description": "Practice acting and put on school performances",
            "schedule": "Fridays, 3:30 PM - 5:30 PM",
            "max_participants": 20,
            "participants": ["ava@mergington.edu", "jacob@mergington.edu"]
        },
        "Robotics Club": {
            "description": "Design and build robots while learning engineering concepts",
            "schedule": "Mondays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 12,
            "participants": ["henry@mergington.edu", "lily@mergington.edu"]
        },
        "Math Team": {
            "description": "Solve challenging math problems and prepare for competitions",
            "schedule": "Tuesdays, 3:30 PM - 5:00 PM",
            "max_participants": 14,
            "participants": ["oliver@mergington.edu", "emma@mergington.edu"]
        }
    }

    activities.clear()
    activities.update(copy.deepcopy(initial_state))
    yield
    activities.clear()
    activities.update(copy.deepcopy(initial_state))


def test_get_activities_returns_activities():
    # Arrange
    client = TestClient(app)

    # Act
    resp = client.get("/activities")

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_for_activity_adds_participant():
    # Arrange
    client = TestClient(app)
    activity = "Chess Club"
    email = "testuser@example.com"
    initial_count = len(activities[activity]["participants"])

    # Act
    path = f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}"
    resp = client.post(path)

    # Assert
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]
    assert len(activities[activity]["participants"]) == initial_count + 1


def test_signup_duplicate_returns_400():
    # Arrange
    client = TestClient(app)
    activity = "Chess Club"
    email = activities[activity]["participants"][0]

    # Act
    path = f"/activities/{urllib.parse.quote(activity)}/signup?email={urllib.parse.quote(email)}"
    resp = client.post(path)

    # Assert
    assert resp.status_code == 400


def test_remove_participant_removes_participant():
    # Arrange
    client = TestClient(app)
    activity = "Chess Club"
    email = activities[activity]["participants"][0]
    initial_count = len(activities[activity]["participants"])

    # Act
    path = f"/activities/{urllib.parse.quote(activity)}/participants?email={urllib.parse.quote(email)}"
    resp = client.delete(path)

    # Assert
    assert resp.status_code == 200
    assert email not in activities[activity]["participants"]
    assert len(activities[activity]["participants"]) == initial_count - 1
