import dacite

from app.core.condition import RuleDirection
from app.core.project import Project
from app.core.providers import Provider, get_provider
from app.core.db import Database
from app.core.rule import Rule, RuleDTO
from dataclasses import asdict
from dacite import from_dict


def get_rules(db: Database) -> list[RuleDTO]:
    rules_dicts: list[dict] = db.get_all("rules")
    type_hooks = {RuleDirection: RuleDirection}

    dtos: list[RuleDTO] = [
        RuleDTO.from_rule(
            from_dict(
                data=x,
                data_class=Rule,
                config=dacite.Config(type_hooks=type_hooks),
            )
        )
        for x in rules_dicts
    ]

    return dtos


def add_rule(rule_dto: RuleDTO, db: Database):
    rule = Rule.from_dto(rule_dto)
    # TODO: return error upon adding of duplicates
    if rule.source.tracker.lower() > rule.destination.tracker.lower():
        rule.source, rule.destination = rule.destination, rule.source
    db.add_row("rules", asdict(rule))
    # TODO: return created rule


def remove_rule(rule_dto: RuleDTO, db: Database):
    rule = Rule.from_dto(rule_dto)
    db.delete("rules", asdict(rule))


def get_projects(tracker: str) -> list[str]:
    provider: Provider = get_provider(tracker)
    projects: list[Project] = provider.get_projects()
    return [x.name for x in projects]
