from fastapi.testclient import TestClient
from app.api.endpoints.rules import router
from app.core.application import create_api
from dotenv import load_dotenv

api = create_api()
api.include_router(router)

client = TestClient(api)

load_dotenv()


TEST_RULES = [
    {
        "source": {
            "tracker": "aaa",
            "board": "bbb",
            "fieldName": "ccc",
            "fieldVal": "ddd",
            "compOp": "=",
        },
        "destination": {
            "tracker": "eee",
            "board": "fff",
            "fieldName": "ggg",
            "fieldVal": "hhh",
            "compOp": "=",
        },
        "direction": "cmp",
    },
    {
        "source": {
            "tracker": "aaa",
            "board": "bbb",
            "fieldName": "ccc",
            "fieldVal": "ddd",
            "compOp": "=",
        },
        "destination": {
            "tracker": "eee",
            "board": "fff",
            "fieldName": "ggg",
            "fieldVal": "hhh",
            "compOp": "=",
        },
        "direction": "std",
    },
    {
        "source": {
            "tracker": "aaa",
            "board": "bbb",
            "fieldName": "ccc",
            "fieldVal": "ddd",
            "compOp": "=",
        },
        "destination": {
            "tracker": "eee",
            "board": "fff",
            "fieldName": "ggg",
            "fieldVal": "hhh",
            "compOp": "=",
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
        assert (
            created_rule["source"]["tracker"]
            == test_rule["source"]["tracker"]
        )
        assert (
            created_rule["source"]["board"] == test_rule["source"]["board"]
        )
        assert (
            created_rule["source"]["fieldName"]
            == test_rule["source"]["fieldName"]
        )
