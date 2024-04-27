from dacite import from_dict
import datetime
from app.core.issues import GitlabIssue, JiraIssue, Issue
from app.core.rule import Rule, RuleSide
from app.core.db import MockDatabase
from app.services.issues import IssuesService


def test_bidirectional_sync():
    db = MockDatabase()
    issues_svc: IssuesService = IssuesService(db)

    src: RuleSide = RuleSide(
        tracker="gitlab",
        board="KAN",
        field="description",
    )

    dest: RuleSide = RuleSide(
        tracker="jira",
        board="KAN",
        field="description",
    )

    rule = Rule(source=src, destination=dest)

    issues = issues_svc.get_issues()
    gitlab_issue: Issue = [x for x in issues if x.issue_name == "hello world"][0]
    jira_issue: Issue = [x for x in issues if x.issue_name == "hello world"][1]

    assert gitlab_issue.description != jira_issue.description

    gitlab_issue, jira_issue = rule.sync(gitlab_issue, jira_issue)

    assert gitlab_issue.description == jira_issue.description
