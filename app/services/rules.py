from app.core.db import Database
from app.core.rule import Rule
from app.core.issues import Issue
from dacite import from_dict


class RulesService:
    def __init__(self, db: Database):
        self._db: Database = db

    def get_rules(self) -> list[Rule]:
        rules_dicts: list[dict] = self._db.get_all("rules")

        rules: list[Rule] = [
            from_dict(data=x, data_class=Rule) for x in rules_dicts
        ]
        return rules

    def get_newer_issue(self, src: Issue, dst: Issue) -> Issue:
        if src.updated_at - dst.updated_at > 0:
            return src
        return dst
