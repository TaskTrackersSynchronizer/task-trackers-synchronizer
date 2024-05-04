from app.core.condition import Condition, RuleDirection, DefaultCondition
from app.core.issues import Issue
from dataclasses import dataclass, field
from datetime import datetime

# Rules for synchronization between source and task trackers


class SyncError(RuntimeError):
    pass


@dataclass
class FieldFilter:
    tracker: str
    board: str
    field_name: str
    field_val: str
    comp_op: str


@dataclass
class RuleDTO:
    source: FieldFilter
    destination: FieldFilter
    direction: RuleDirection

    # TODO: handle comp_op for conditions
    @classmethod
    def from_rule(cls, rule: "Rule") -> "RuleDTO":
        dto = cls(
            source=FieldFilter(
                tracker=rule.source.tracker,
                board=rule.source.project,
                field_name=rule.source.field,
                # Used for conditional rules, not supported
                comp_op="",
                field_val="",
            ),
            destination=FieldFilter(
                tracker=rule.destination.tracker,
                board=rule.destination.project,
                field_name=rule.destination.field,
                # Used for conditional rules, not supported
                comp_op="",
                field_val="",
            ),
            # Used for conditional rules, not supported
            direction=RuleDirection.ANY,
        )
        return dto


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

    def is_synced(self, src_issue: Issue, dst_issue: Issue) -> bool:
        # TODO: handle condition
        # if self.condition is None:

        if src_issue is None and dst_issue is None:
            raise ValueError("At leat one of issues must not be NoneType")

        if dst_issue is None or src_issue is None:
            return False

        return getattr(src_issue, self.source.field) == getattr(
            dst_issue, self.destination.field
        )

    def sync(self, src_issue: Issue, dst_issue: Issue) -> tuple[Issue, Issue]:
        if not self.condition or self.condition.condition_type == "default":
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
