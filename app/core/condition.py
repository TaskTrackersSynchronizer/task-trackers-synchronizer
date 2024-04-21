import abc


class Condition(abc.ABC):
    """Interface for the sync condition"""
    def test() -> bool:
        return True


class SimpleFieldCondition(Condition):
   pass
    mock_val = {
            "type": "equality",
            "data": {
                "source_value": "In progress",
                "destination_value": "Doing",
                "direction": 0,
                }
            }

