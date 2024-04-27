from fastapi import APIRouter

from app.core.logger import logger
from app.core.providers import Provider, get_provider

router = APIRouter()


# Board id reserved for specific trackers which might have differnet fields per project
@router.get("/fields/{tracker}")
def get_fields(tracker: str, board: Optional[str]):
    provider: Provider = get_provider(tracker)
    if provider is None:
        logger.error(f"Provider {tracker} is not found")
        return []
