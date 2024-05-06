from fastapi import APIRouter
from app.api.crud import get_projects

router = APIRouter(prefix="/api")


@router.get("/boards")
def get_boards(tracker: str = "Gitlab"):
    return get_projects(tracker)
