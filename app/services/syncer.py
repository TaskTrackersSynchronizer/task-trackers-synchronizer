from app.services.issues import IssuesService
from app.services.rules import RulesService
from app.core.rule import Rule
from app.core.issues import Issue
from app.core.providers import get_provider
from app.core.db import DocumentDatabase
from datetime import datetime
from app.core.providers import Provider
from dataclasses import dataclass, field
from typing import Optional
from app.core.logger import logger
from collections import defaultdict


@dataclass
class ProviderPair:
    src: Provider
    dst: Provider


@dataclass
class ProjectNamePair:
    src_project: str
    dst_project: str
    src_provider: Provider
    dst_provider: Provider
    rules: list[Rule] = field(default_factory=list)
    issues: list[Issue] = field(default_factory=list)


class Syncer:
    def __init__(self, db: DocumentDatabase) -> None:
        self.rules_svc = RulesService(db)
        self.issues_svc = IssuesService(db)
        # todo: renew updated at

        # assme that issues are never synced at the beginning
        self.updated_at = datetime.fromtimestamp(0)

    # TODO: cache
    def get_project_name_pairs_from_rules(
        self, rules: list[Rule], src_tracker: str, dst_tracker: str
    ) -> list[ProjectNamePair]:
        relevant_projects: list[ProjectNamePair] = []
        projects_dict: dict[
            tuple[str, str], list[Rule]
        ] = defaultdict(list)

        logger.debug(
            f"get_project_name_pairs_from_rules rules: {rules}"
        )
        logger.debug(
            f"""get_project_name_pairs_from_rules\
            src_tracker: {src_tracker},\
            dst_tracler: {dst_tracker}"""
        )
        rule: Rule
        for rule in rules:
            if (
                rule.source.tracker.lower() == src_tracker.lower()
                and rule.destination.tracker.lower()
                == dst_tracker.lower()
            ):
                projects_dict[
                    (rule.source.project, rule.destination.project)
                ].append(rule)

        logger.info(projects_dict)
        for projects_pair, rules in projects_dict.items():
            relevant_projects.append(
                ProjectNamePair(
                    src_project=projects_pair[0],
                    dst_project=projects_pair[1],
                    rules=rules,
                    src_provider=get_provider(src_tracker),
                    dst_provider=get_provider(dst_tracker),
                )
            )

        return relevant_projects

    # - assume script runs quick enough so issue is updated only at one side
    # - assume issues between two projects within same provider are not synced
    # - assume there can be only one related issue
    #   in a pair of two  project providers
    def handle_updated_issues(self, projects_pairs: ProjectNamePair):
        projects_pairs.issues.sort(key=lambda x: x.updated_at)
        assert len(projects_pairs.issues) > 0
        assert len(projects_pairs.rules) > 0
        for rule in projects_pairs.rules:
            for issue in projects_pairs.issues:
                # TODO: make database issue provider
                # TODO: fetch local

                # TODO: for each issue keep set of related ids
                related_issue: Optional[
                    Issue
                ] = self.issues_svc.get_related_issue(
                    issue,
                    rule.destination.project,
                    projects_pairs.dst_provider,
                )
                if related_issue is None:
                    related_issue = (
                        projects_pairs.dst_provider.create_issue(
                            rule.destination.project,
                            issue.issue_name,
                        )
                    )

                    related_issue.import_values(
                        issue.export_values(unconvert=False),
                        convert=False,
                    )

                    related_issue.update()

                else:
                    rule.sync(issue, related_issue)

        pass

    def sync_all(self) -> None:
        # TODO: parametrize list of providers

        # TODO: order source and target
        rules: list[Rule] = self.rules_svc.get_rules()

        # TODO: parametrize unique pairs of providers
        ordered_providers: list[str] = [("gitlab", "jira")]

        # TODO: ensure that all pairs are ordered
        for providers_pair in ordered_providers:
            projects_pairs: list[
                ProjectNamePair
            ] = self.get_project_name_pairs_from_rules(
                rules, providers_pair[0], providers_pair[1]
            )

            for projects_pair in projects_pairs:
                projects_pair.issues += (
                    projects_pair.src_provider.get_project_issues(
                        projects_pair.src_project,
                        updated_at=self.updated_at,
                    )
                )

                projects_pair.issues += (
                    projects_pair.dst_provider.get_project_issues(
                        projects_pair.dst_project,
                        updated_at=self.updated_at,
                    )
                )

                self.handle_updated_issues(projects_pair)

        self.updated_at = datetime.now()
