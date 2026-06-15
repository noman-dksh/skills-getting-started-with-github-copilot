import pytest


@pytest.mark.asyncio
async def test_root_redirect(async_client):
    # Arrange
    url = "/"

    # Act
    resp = await async_client.get(url, follow_redirects=False)

    # Assert
    assert resp.status_code == 307
    assert resp.headers.get("location") == "/static/index.html"
