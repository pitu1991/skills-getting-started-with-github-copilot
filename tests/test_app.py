def test_get_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"
    assert "participants" in data["Chess Club"]


def test_signup_for_activity(client):
    response = client.post(
        "/activities/Chess%20Club/signup?email=teststudent@mergington.edu"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Signed up teststudent@mergington.edu for Chess Club"

    participants = client.get("/activities").json()["Chess Club"]["participants"]
    assert "teststudent@mergington.edu" in participants


def test_signup_duplicate_fails(client):
    response = client.post(
        "/activities/Programming%20Class/signup?email=emma@mergington.edu"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_remove_participant(client):
    response = client.delete(
        "/activities/Chess%20Club/participants?email=michael@mergington.edu"
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Removed michael@mergington.edu from Chess Club"

    participants = client.get("/activities").json()["Chess Club"]["participants"]
    assert "michael@mergington.edu" not in participants


def test_remove_missing_participant_returns_404(client):
    response = client.delete(
        "/activities/Chess%20Club/participants?email=missing@student.edu"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
