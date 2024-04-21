from typing import List
from fastapi import APIRouter

from app.core.logger import logger

router = APIRouter()


# Retrieve initial data regarding task trackers.
# Might include fields or something like List[BoardInfo]
# BoardInfo: List[BoardField]
# For the mock on front we can assume that initial data is present
@router.get("/trackers/")
def get_trackers(flat: bool = True):
    logger.info("Mock get trackers")
    return ["Notion", "TaskWarrior"]
