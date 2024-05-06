import os

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.staticfiles import StaticFiles

from app.api.endpoints import fields_mock, rules_mock, trackers_mock
from app.api.endpoints import fields, rules, trackers, projects
from app.services.syncer import Syncer
from app.core.db import DocumentDatabase
from threading import Timer

STATIC_RESOURCES = os.environ.get("STATIC_RESOURCES", "/app/static")
TIMEOUT = float(os.environ.get("TIMEOUT", "60.0"))
DATABASE_URL = os.environ.get("DATABASE_URL", ":memory:")


class RepeatTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


def _create_sync_task():
    syncer = Syncer(DocumentDatabase(DATABASE_URL))
    timer = RepeatTimer(TIMEOUT, lambda: syncer.sync_all())
    timer.start()


def create_api():
    api = FastAPI()
    Instrumentator().instrument(api).expose(api)

    api.include_router(rules.router)
    api.include_router(fields.router)
    api.include_router(trackers.router)
    api.include_router(projects.router)

    api.mount(
        "/",
        StaticFiles(directory=STATIC_RESOURCES, html=True),
        name="static",
    )

    _create_sync_task()

    return api


def create_mock_api() -> FastAPI:
    api = FastAPI()
    Instrumentator().instrument(api).expose(api)

    api.include_router(fields_mock.router)
    api.include_router(rules_mock.router)
    api.include_router(trackers_mock.router)

    api.mount(
        "/",
        StaticFiles(directory=STATIC_RESOURCES, html=True),
        name="static",
    )

    return api
