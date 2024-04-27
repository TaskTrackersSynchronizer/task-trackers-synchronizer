from dataclasses import dataclass
from typing import Optional
from app.core.condition import Condition
from datetime import datetime
from app.core.issues import Issue

# Rules for synchronization between source and task trackers


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

    # todo move somewhere
    def get_newer_issue(self, src: Issue, dst: Issue) -> Issue:
        return dst

    def sync(self, src_issue: Issue, dst_issue: Issue):
        if self.condition is None:
            newer: Issue
            older: Issue

            # datetime.strptime(datetime_str, '%Y-%m-%dT%H:%M:%S.%f%z')

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

            setattr(older, self.source.field, getattr(newer, self.destination.field))

        return src_issue, dst_issue

    # if sync.

    #     "source": {
    #     "tracker": "Notion",
    #     "board": "Task Trackers Synchronizer",
    #     "field": "Summary",
    # },
    # "destination": {
    #     "tracker": "TaskWarrior",
    #     "board": "TTS",
    #     "field": "Description",
    # },
    # # default - bidirectional sync
    # "condition": None,
    #
