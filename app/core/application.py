from fastapi import FastAPI

from app.api.endpoints import fields_mock, rules_mock, trackers_mock


def create_api():
    api = FastAPI()

    # api.include_router(hello.router)

    return api


def create_mock_api() -> FastAPI:
    api = FastAPI()

    api.include_router(fields_mock.router)
    api.include_router(rules_mock.router)
    api.include_router(trackers_mock.router)

    return api
