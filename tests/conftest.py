import copy

import pytest
from httpx import AsyncClient

from src.app import app, activities


@pytest.fixture(autouse=True)
def reset_activities():
    """Ensure the in-memory `activities` dict is restored after each test.

    This fixture follows Arrange-Act-Assert implicitly by returning the
    application state to a known baseline after each test.
    """
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)


@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client
