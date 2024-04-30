from app.core.db import Database
from app.core.rule import Rule
from app.core.issues import Issue
from app.core.application import create_api, create_mock_api

from dacite import from_dict


def get_rules(db: Database) -> list[Rule]:
    rules_dicts: list[dict] = db.get_all("rules")
    rules: list[Rule] = [from_dict(data=x, data_class=Rule) for x in rules_dicts]
    return rules


def add_rule(db: Database, rule: Rule):
    if rule.source.tracker.lower() > rule.destination.tracker.lower():
        rule.source, rule.destination = rule.destination, rule.source
    db.add_row("issues", from_dict(data=rule, data_class=Rule))


class RulesService:
    def __init__(self, db: Database):
        self._db: Database = db

    def get_rules(self) -> list[Rule]:
        return get_rules(self._db)

    def add_rule(self, rule: Rule):
        return add_rule(self._db, rule)
