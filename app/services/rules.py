from app.core.db import Database
from app.core.rule import Rule
from app.core.issues import Issue
from dacite import from_dict


class RulesService:
    def __init__(self, db: Database):
        self._db: Database = db

    def get_rules(self) -> list[Rule]:
        rules_dicts: list[dict] = self._db.get_all("rules")

        rules: list[Rule] = [from_dict(data=x, data_class=Rule) for x in rules_dicts]

        for rule in rules:
            if rule.source.tracker.lower() > rule.destination.tracker.lower():
                rule.source, rule.destination = rule.destination, rule.source

        return rules

    def add_rule(self, rule: Rule):
        if rule.source.tracker.lower() > rule.destination.tracker.lower():
            rule.source, rule.destination = rule.destination, rule.source
        self._db.add_row("issues", from_dict(data=rule, data_class=Rule))

    def get_newer_issue(self, src: Issue, dst: Issue) -> Issue:
        if src.updated_at - dst.updated_at > 0:
            return src
        return dst
