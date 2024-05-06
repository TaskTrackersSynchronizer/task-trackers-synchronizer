from fastapi import APIRouter

from app.core.logger import logger

router = APIRouter(prefix="/api")


@router.get("/")
def read_root():
    logger.info("This is an example of logging")
    return {"hello": "world"}
