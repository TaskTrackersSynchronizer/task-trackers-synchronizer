from typing import Generator

import pytest
from fastapi.testclient import TestClient

from app.core.application import create_mock_api


@pytest.fixture(scope="module")
def mock_client() -> Generator:
    api = create_mock_api()
    with TestClient(api) as c:
        yield c
