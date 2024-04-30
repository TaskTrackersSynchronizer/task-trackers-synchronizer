import pytest
from app.services.syncer import Syncer
from app.core.providers import JiraProvider, GitlabProvider
from app.services.issues import IssuesService
from app.core.issues import Issue, IssuePair
from app.core.db import MockDatabase
from app.core.providers import get_provider
from app.services.rules import RulesService


# 1. get all gitlab, jira issues (optionally older than specified timestamp)
# 2. assert that some fields are not equal
# 3. call sync_all
# 4. assert that fields are synced
# 5. import old values to the issues
# 6. update issues to contain old values
def test_syncs_existing():
    db = MockDatabase()
    syncer: Syncer = Syncer(db)

    rules_svc: RulesService = RulesService(db)

    rules: list[Rule] = rules_svc.get_rules()
    jira_provider = get_provider("Jira")
    gitlab_provider = get_provider("Gitlab")

    def get_unsynced_issues(src_issues, dst_issues) -> list[Issue]:
        related_issues: list[IssuePair] = Issue.filter_related(src_issues, dst_issues)
        unsynced_issues = []
        for rule in rules:
            for issue_pair in related_issues:
                if not rule.is_synced(issue_pair.src, issue_pair.dst):
                    unsynced_issues.append(issue_pair.src)
                    unsynced_issues.append(issue_pair.dst)
        return unsynced_issues

    old_jira_issues: list[JiraIssue] = jira_provider.get_issues("")
    old_gitlab_issues: list[GitlabIssue] = gitlab_provider.get_issues("")

    old_jira_issues_map = {x.issue_name: x for x in old_jira_issues}
    old_gitlab_issues_map = {x.issue_name: x for x in old_gitlab_issues}

    unsynced: list[Issue] = get_unsynced_issues(old_jira_issues, old_gitlab_issues)

    assert len(unsynced) != 0

    syncer.sync_all()

    jira_issues: list[JiraIssue] = jira_provider.get_issues()
    gitlab_issues: list[GitlabIssue] = gitlab_provider.get_issues()

    unsynced: list[Issue] = get_unsynced_issues(jira_issues, gitlab_issues)

    assert len(unsynced) == 0

    def recover_issues(issues, old_issues_map):
        for issue in issues:
            issue.import_values(old_issues_map[issue.issue_name].export_values())
            issue.update()

    recover_issues(jira_issues, old_jira_issues_map)
    recover_issues(gitlab_issues, old_gitlab_issues_map)
