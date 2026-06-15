import pytest
from urllib.parse import quote


@pytest.mark.asyncio
async def test_get_activities(async_client):
    # Arrange
    url = "/activities"

    # Act
    resp = await async_client.get(url)

    # Assert
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


@pytest.mark.asyncio
async def test_signup_and_unregister_flow(async_client):
    # Arrange
    activity_name = quote("Chess Club", safe="")
    signup_url = f"/activities/{activity_name}/signup"
    unregister_url = f"/activities/{activity_name}/participants"
    email = "tester@example.com"

    # Act - signup
    resp_signup = await async_client.post(signup_url, params={"email": email})

    # Assert signup
    assert resp_signup.status_code == 200
    activities = (await async_client.get("/activities")).json()
    assert email in activities["Chess Club"]["participants"]

    # Act - unregister
    resp_unreg = await async_client.delete(unregister_url, params={"email": email})

    # Assert unregister
    assert resp_unreg.status_code == 200
    activities = (await async_client.get("/activities")).json()
    assert email not in activities["Chess Club"]["participants"]


@pytest.mark.asyncio
async def test_signup_existing_email_returns_400(async_client):
    # Arrange
    activity_name = quote("Chess Club", safe="")
    signup_url = f"/activities/{activity_name}/signup"
    existing_email = "michael@mergington.edu"

    # Act
    resp = await async_client.post(signup_url, params={"email": existing_email})

    # Assert
    assert resp.status_code == 400


@pytest.mark.asyncio
async def test_signup_unknown_activity_returns_404(async_client):
    # Arrange
    activity_name = quote("Nonexistent Activity", safe="")
    signup_url = f"/activities/{activity_name}/signup"

    # Act
    resp = await async_client.post(signup_url, params={"email": "x@y.com"})

    # Assert
    assert resp.status_code == 404


@pytest.mark.asyncio
async def test_unregister_nonexistent_participant_returns_404(async_client):
    # Arrange
    activity_name = quote("Chess Club", safe="")
    unregister_url = f"/activities/{activity_name}/participants"

    # Act
    resp = await async_client.delete(unregister_url, params={"email": "noone@example.com"})

    # Assert
    assert resp.status_code == 404
