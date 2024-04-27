from app.core.db import Database
from app.core.rule import Rule
from app.core.issues import Issue
from app.services.issues import IssuesService
from typing import List, Dict
from dacite import from_dict


class RulesService:
    def __init__(self, db: Database):
        self._db: Database = db

    def get_rules(self) -> List[Rule]:
        rules_dicts: List[Dict] = self._db.get("rules")
        rules: List[Rule] = [from_dict(x, dataclass=Rule) for x in rules_dicts]
        return rules

    def get_newer_issue(self, src: Issue, dst: Issue) -> Issue:
        if src.updated_at - dst.updated_at > 0:
            return src
        return dst

    def sync(self, src_issue: Issue, dst_issue: Issue):
        if self.condition is None:
            newer: Issue = self.get_newer_issue(src_issue, dst_issue)
