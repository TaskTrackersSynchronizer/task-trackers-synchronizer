import abc
from dataclasses import dataclass

from enum import Enum


class RuleDirection(str, Enum):
    SRC_TO_DEST = "std"
    DEST_TO_SRC = "dts"
    ANY = "any"


@dataclass
class Condition(abc.ABC):
    """Interface for the sync condition"""

    condition_type: str = "default"
    direction: RuleDirection = RuleDirection.ANY

    def test(self) -> bool:
        return True

    # mock_val = {
    #         "type": "equality",
    #         "data": {
    #             "source_value": "In progress",
    #             "destination_value": "Doing",
    #             "direction": 0,
    #             }
    #         }
    #


@dataclass
class FieldEqualityCondition(Condition):
    source_value: str = ""
    destination_value: str = ""
    condition_type: str = "equality"

    def test(self) -> bool:
        return self.source_value == self.destination_value
