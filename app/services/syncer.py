from app.services.issues import IssuesService
from collections import defaultdict
from app.services.rules import RulesService
from app.core.rule import Rule
from app.core.issues import Issue
from app.core.providers import get_provider
from app.core.db import DocumentDatabase
from itertools import groupby
from datetime import datetime
from app.core.providers import JiraProvider, GitlabProvider, Provider
from dataclasses import dataclass
from typing import Optional


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
    rules: list[Rule]
    issues: list[Issue]
    

class Syncer:
    def __init__(self, db: DocumentDatabase) -> None:
        # self.jira_db = DocumentDatabase(":memory:")
        # self.gitlab_db = DocumentDatabase(":memory:")
        # todo: use same db
        # self.jira_provider: JiraProvider = get_provider(name="jira")
        # self.gitlab_provider: GitlabProvider = get_provider(name="gitlab")
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
        projects_dict: dict[tuple[str, str], list[Rule]] = defaultdict(list)
        rule: Rule
        # print(
        #     f"get_project_name_pairs_from_rule: src_tracker: {src_tracker}, dst_tracker: {dst_tracker}"
        # )
        for rule in rules:
            print(rule)
            # print(
            #         f"rule: src_tracker: {rule.source.tracker}, dst_tracker: {rule.destination.tracker}, src_board: {rule.}"
            # )
            if (
                rule.source.tracker.lower() == src_tracker.lower()
                and rule.destination.tracker.lower() == dst_tracker.lower()
            ):
                projects_dict[(rule.source.board, rule.destination.board)].append(rule)

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

    def handle_updated_issues(
        self, projects: ProjectNamePair, updated_issues: list[Issue]
    ):
        for rule in projects.rules:
            for issue in updated_issues:
                # TODO: make database issue provider
                # TODO: fetch local
                related_issue: Optional[Issue] = self.issues_svc.get_related_issue(
                    issue, projects.dst_provider
                )
                if related_issue is None:
                    # related issue didn't exist
                    # creation is needed
                    pass
                else:
                    rule.sync(issue, related_issue)

        pass

    def sync_all(self) -> None:
        # TODO: parametrize list of providers
        # jira_issues = self.jira_provider.get_last_updated_issues(self.updated_at)
        # gitlab_issues = self.gitlab_provider.get_last_updated_issues(self.updated_at)

        # TODO: order source and target
        rules: list[Rule] = self.rules_svc.get_rules()

        # TODO: parametrize unique increasingly ordered pairs of providers
        ordered_providers: list[str] = [("Gitlab", "Jira")]

        # TODO: ensure that all pairs are ordered
        for providers_pair in ordered_providers:
            src_provider: Provider = get_provider(providers_pair[0])
            dst_provider: Provider = get_provider(providers_pair[1])
            assert src_provider is not None
            assert dst_provider is not None
            projects_pairs: list[
                ProjectNamePair
            ] = self.get_project_name_pairs_from_rules(
                rules, providers_pair[0], providers_pair[1]
            )

            # for pp in projects_pairs:
            #     if pp.src_project 

            # src_issues = src_provider.get_last_updated_issues(self.updated_at)
            # dst_issues = dst_provider.get_last_updated_issues(self.updated_at)
            # 1. group by rules
            
            src_project_issues = []
            dst_project_issues = []
            # for proj_name, issues in groupby(src_issues, lambda x: x[0]):
            #     for thing in group:
            #         print("A %s is a %s." % (thing[1], key))
            
            src_project_issues = src_issues.

            recently_updated_issues = src_issues + dst_issues

            # assuming source and target projects are defined
            # assumed that
            # out: List[issues]

        # for _, group in groupby(issues, key=lambda x: x.issue_name):
        #     src, dest = group[0], group[1]
        #
        #     for rule in rules:
        #         rule.sync(src, dest)

        self.updated_at = datetime.now()
