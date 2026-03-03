import pytest
from fastapi.testclient import TestClient

from kotoba_api.app import app


@pytest.fixture(scope="session")
def client():
    return TestClient(app)
