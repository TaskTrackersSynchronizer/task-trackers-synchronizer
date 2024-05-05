# Returns list of supported task trackers.
# Might be hardcoded on frontend if necessary

from fastapi import APIRouter
from app.core.config import config

import typing as t

router = APIRouter(prefix="/api")


# Retrieve initial data regarding task trackers.
# Might include fields or something like List[projectInfo]
# projectInfo: List[projectField]
# For the mock on front we can assume that initial data is present
@router.get("/trackers/")
def get_trackers(flat: t.Optional[bool] = True):
    return config.trackers
