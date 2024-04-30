from app.core.condition import Condition, RuleDirection, DefaultCondition
from app.core.issues import Issue
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime
from pydantic import BaseModel

# Rules for synchronization between source and task trackers


class SyncError(RuntimeError):
    pass


@dataclass
class FieldFilter(BaseModel):
    tracker: str
    board: str
    field_name: str
    field_val: str
    comp_op: str


@dataclass
class RuleDTO(BaseModel):
    source: FieldFilter
    destination: FieldFilter
    direction: RuleDirection


# export class SyncRule {
#     source: FieldFilter;
#     destination: FieldFilter;
#     direction: SyncDirection;
# }


@dataclass
class RuleSide:
    tracker: str
    project: str
    field: str


@dataclass
class Rule:
    source: RuleSide
    destination: RuleSide
    condition: Condition = field(default_factory=DefaultCondition)

    @classmethod
    def from_dto(cls, dto: RuleDTO) -> "Rule":
        # TODO: parse condition
        rule = cls(
            source=RuleSide(
                tracker=dto.source.tracker,
                project=dto.source.board,
                field=dto.source.field_name,
            ),
            destination=RuleSide(
                tracker=dto.source.tracker,
                project=dto.source.board,
                field=dto.source.field_name,
            ),
            condition=DefaultCondition(),
        )
        return rule

    def is_synced(self, src_issue: Issue, dst_issue: Issue):
        # TODO: handle condition
        # if self.condition is None:

        if getattr(src_issue, self.source.field) == getattr(
            dst_issue, self.destination.field
        ):
            return True
        return False

    def sync(self, src_issue: Issue, dst_issue: Issue) -> tuple[Issue, Issue]:
        if self.condition is None or self.condition.condition_type == "default":
            newer: Issue
            older: Issue

            src_updated_at = src_issue.updated_at
            dst_updated_at = dst_issue.updated_at

            if isinstance(src_updated_at, str):
                src_updated_at = datetime.strptime(
                    src_updated_at, "%Y-%m-%dT%H:%M:%S.%f%z"
                )
                dst_updated_at = datetime.strptime(
                    dst_updated_at, "%Y-%m-%dT%H:%M:%S.%f%z"
                )
            if src_updated_at > dst_updated_at:
                newer, older = src_issue, dst_issue
            else:
                newer, older = dst_issue, src_issue

            setattr(
                older,
                self.source.field,
                getattr(newer, self.destination.field),
            )

            older.update()
        # TODO: handle condition testing
        elif self.condition.direction == RuleDirection.SRC_TO_DEST:
            setattr(
                dst_issue,
                self.source.field,
                getattr(src_issue, self.destination.field),
            )
        elif self.condition.direction == RuleDirection.DEST_TO_SRC:
            setattr(
                src_issue,
                self.source.field,
                getattr(dst_issue, self.destination.field),
            )

        else:
            raise SyncError("Unable to resolve sync rule")

        return src_issue, dst_issue
