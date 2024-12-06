# conftest.py
import pytest
from rest_framework.test import APIClient

@pytest.fixture
def api_client():
    """Fixture for setting up an API client."""
    return APIClient()
