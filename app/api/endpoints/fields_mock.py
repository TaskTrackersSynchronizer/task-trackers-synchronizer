from fastapi import APIRouter
from typing import Optional
from app.core.logger import logger

router = APIRouter()


@router.get("/fields/")
def get_fields(tracker: str, board: Optional[str]):
    logger.info("Mock get fields")
    return [
        "Name",
        "Tags",
        "Summary",
        "Done?",
        "Depends on",
    ]
