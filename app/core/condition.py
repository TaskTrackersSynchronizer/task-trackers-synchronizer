from dataclasses import dataclass
from abc import ABC, abstractmethod

from enum import Enum


class RuleDirection(str, Enum):
    SRC_TO_DEST = "std"
    DEST_TO_SRC = "dts"
    ANY = "any"


@dataclass
class Condition(ABC):
    """Interface for the sync condition"""

    condition_type: str = "default"
    direction: RuleDirection = RuleDirection.ANY

    @abstractmethod
    def test(self) -> bool:
        return True


@dataclass
class FieldEqualityCondition(Condition):
    source_value: str = ""
    destination_value: str = ""
    condition_type: str = "equality"

    def test(self) -> bool:
        return self.source_value == self.destination_value
