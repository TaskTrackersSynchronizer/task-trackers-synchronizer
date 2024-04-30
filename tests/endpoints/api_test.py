from fastapi.testclient import TestClient
from app.api.endpoints.rules import router
from fastapi import FastAPI

api = FastAPI()
api.include_router(router)

client = TestClient(api)


def test_adds_rule():
    rule = {
        "source": {
            "tracker": "aaa",
            "board": "bbb",
            "field_name": "ccc",
            "field_val": "ddd",
            "comp_op": "=",
        },
        "destination": {
            "tracker": "eee",
            "board": "fff",
            "field_name": "ggg",
            "field_val": "hhh",
            "comp_op": "=",
        },
        "direction": "cmp",
    }

    # return
    response = client.post("/api/add_rule", json=rule)
    assert response.status_code == 200
