from services.issues import IssuesService
from services.rules import RulesService
from db import DocumentDatabase
from itertools import groupby


class Syncer:
    def __init__(self) -> None:
        self.jira_db = DocumentDatabase(":memory:")
        self.gitlab_db = DocumentDatabase(":memory:")
        self.jira_issues_svc = IssuesService(self.jira_db)
        self.gitlab_issues_svc = IssuesService(self.jira_db)
        self.rules_svc = RulesService(self.gitlab_db)

    def sync_all(self) -> None:
        jira_issues = self.jira_issues_svc.get_issues()
        gitlab_issues = self.gitlab_issues_svc.get_issues()
        issues = jira_issues + gitlab_issues

        rules = self.rules_svc.get_rules()

        for _, group in groupby(issues, key=lambda x: x.issue_name):
            src, dest = group[0], group[1]

            for rule in rules:
                rule.sync(src, dest)
        
