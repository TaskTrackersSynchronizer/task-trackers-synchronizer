import os

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.staticfiles import StaticFiles

from app.api.endpoints import fields_mock, rules_mock, trackers_mock
from app.api.endpoints import fields, rules, trackers, projects
from fastapi import BackgroundTasks
from app.core.db import get_db
from app.services.syncer import Syncer

static_resources_path = os.getenv("STATIC_RESOURCES", "/app/static")


def create_api():
    api = FastAPI()
    Instrumentator().instrument(api).expose(api)

    api.include_router(rules.router)
    api.include_router(fields.router)
    api.include_router(trackers.router)
    api.include_router(projects.router)

    api.mount(
        "/",
        StaticFiles(directory=static_resources_path, html=True),
        name="static",
    )

    tasks = BackgroundTasks()
    syncer: Syncer = Syncer(get_db())
    tasks.add_task(syncer.start)
    return api


def create_mock_api() -> FastAPI:
    api = FastAPI()
    Instrumentator().instrument(api).expose(api)

    api.include_router(fields_mock.router)
    api.include_router(rules_mock.router)
    api.include_router(trackers_mock.router)

    api.mount(
        "/",
        StaticFiles(directory=static_resources_path, html=True),
        name="static",
    )

    return api
