import os

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.endpoints import fields_mock, rules_mock, trackers_mock
from app.api.endpoints import fields, rules, trackers

static_resources_path = os.getenv("STATIC_RESOURCES", "/app/static")


def create_api():
    api = FastAPI()
    Instrumentator().instrument(api).expose(api)

    api.include_router(rules.router)
    api.include_router(fields.router)
    api.include_router(trackers.router)

    return api


def create_mock_api() -> FastAPI:
    api = FastAPI()
    Instrumentator().instrument(api).expose(api)

    api.include_router(fields_mock.router)
    api.include_router(rules_mock.router)
    api.include_router(trackers_mock.router)

    return api
