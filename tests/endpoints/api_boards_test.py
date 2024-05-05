from fastapi.testclient import TestClient
from app.api.endpoints.projects import router
from fastapi import FastAPI

api = FastAPI()
api.include_router(router)

client = TestClient(api)


def test_get_boards():
    response = client.get("/api/boards?tracker=Gitlab")

    assert response.status_code == 200

    projects = response.json()

    assert len(projects) == 1
    assert projects[0] == "KAN"
