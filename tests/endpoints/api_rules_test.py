from fastapi.testclient import TestClient
from app.api.endpoints.rules import router
from fastapi import FastAPI
from app.core.logger import logger
from dotenv import load_dotenv

api = FastAPI()
api.include_router(router)

client = TestClient(api)

load_dotenv()


TEST_RULES = [
    {
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
    },
    {
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
        "direction": "std",
    },
    {
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
        "direction": "dts",
    },
]


def test_add_remove_rule():
    rule = TEST_RULES[0]
    # return
    response = client.post("/api/add_rule", json=rule)
    assert response.status_code == 200

    client.request("DELETE", "/api/remove_rule", json=rule)
    assert response.status_code == 200


def test_get_rules():
    for rule in TEST_RULES:
        response = client.post("/api/add_rule", json=rule)
        assert response.status_code == 200

    response = client.get("/api/rule_list")
    assert response.status_code == 200
    created_rules = response.json()
    assert (
        len(created_rules) == len(TEST_RULES)
        or len(created_rules) == len(TEST_RULES) + 1
    )

    for created_rule, test_rule in zip(created_rules, TEST_RULES):
        assert created_rule["source"]["tracker"] == test_rule["source"]["tracker"]
        assert created_rule["source"]["board"] == test_rule["source"]["board"]
        assert created_rule["source"]["field_name"] == test_rule["source"]["field_name"]
