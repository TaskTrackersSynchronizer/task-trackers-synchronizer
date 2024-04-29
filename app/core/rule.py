from app.core.condition import Condition, RuleDirection
from app.core.issues import Issue
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

# Rules for synchronization between source and task trackers


class SyncError(RuntimeError):
    pass


@dataclass
class RuleSide:
    tracker: str
    board: str
    field: str


@dataclass
class Rule:
    source: RuleSide
    destination: RuleSide
    condition: Optional[Condition] = None

    def sync(self, src_issue: Issue, dst_issue: Issue) -> tuple[Issue, Issue]:
        if self.condition is None:
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
