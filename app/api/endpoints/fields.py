from fastapi import APIRouter

from app.core.logger import logger

router = APIRouter()


# TODO: return supported fields for requested task tracker / board for suggestion. In initial implementation it
# will return only list of supported fields without types
@router.get("/fields/")
def get_fields(tracker: str, board: Optional[str]):
    logger.info("get fields")
    pass
