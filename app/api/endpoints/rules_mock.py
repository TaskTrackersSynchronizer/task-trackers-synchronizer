from fastapi import APIRouter

from app.core.logger import logger

router = APIRouter()


@router.post("/rules/")
def add_rule():
    return {}


@router.get("/rules/")
def get_rules():
    logger.info("Mock get rules")
    return [
        {
            "source": {
                "tracker": "Notion",
                "board": "Task Trackers Synchronizer",
                "field": "Summary",
            },
            "destination": {
                "tracker": "TaskWarrior",
                "board": "TTS",
                "field": "Description",
            },
            "condition": None,
        },
        {
            "source": {
                "tracker": "Notion",
                "board": "Task Trackers Synchronizer",
                "field": "Tags",
            },
            "destination": {
                "tracker": "TaskWarrior",
                "board": "TTS",
                "field": "Tags",
            },
            "condition": None,
        },
        {
            "source": {
                "tracker": "Notion",
                "board": "Task Trackers Synchronizer",
                "field": "Tags",
            },
            "destination": {
                "tracker": "TaskWarrior",
                "board": "TTS",
                "field": "Tags",
            },
            # If source value is equal "In progress", set destination value to "Doing". Since direction is 0 (Left to right), perform sync only if source value is changed
            "condition": {
                "direction": 0,
                "data": {
                    "type": "equality",
                    "source_value": "In progress",
                    "destination_value": "Doing",
                },
            },
        },
    ]
