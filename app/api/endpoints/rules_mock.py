from fastapi import APIRouter

from app.core.logger import logger

router = APIRouter()


@router.post("/rules/")
def add_rule():
    return {}


# TODO: resolve src, target trackers by rule attrs
# @router.delete("/rules/")
# def remove_rule(rule: Dict):
#     return {}


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
            # default - bidirectional sync
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
                "type": "equality",
                "source_value": "In progress",
                "destination_value": "Doing",
                "direction": "std",  # source to destination
            },
        },
    ]
