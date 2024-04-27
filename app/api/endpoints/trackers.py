# Returns list of supported task trackers.
# Might be hardcoded on frontend if necessary

from typing import List
from typing import Optional
from fastapi import APIRouter
from app.core.config import config

router = APIRouter()


# Retrieve initial data regarding task trackers.
# Might include fields or something like List[BoardInfo]
# BoardInfo: List[BoardField]
# For the mock on front we can assume that initial data is present
@router.get("/trackers/")
def get_trackers(flat: Optional[bool] = True):
    return config.trackers
