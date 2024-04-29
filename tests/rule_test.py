from app.core.issues import Issue
from app.core.rule import Rule, RuleSide
from app.core.db import MockDatabase
from app.services.issues import IssuesService
from app.core.condition import FieldEqualityCondition, RuleDirection


def test_bidirectional_sync():
    db = MockDatabase()
    issues_svc: IssuesService = IssuesService(db)

    src: RuleSide = RuleSide(
        tracker="gitlab",
        project="KAN",
        field="description",
    )

    dest: RuleSide = RuleSide(
        tracker="jira",
        project="KAN",
        field="description",
    )

    rule = Rule(source=src, destination=dest)

    issues = issues_svc.get_issues()
    gitlab_issue: Issue = [x for x in issues if x.issue_name == "hello world"][0]
    jira_issue: Issue = [x for x in issues if x.issue_name == "hello world"][1]

    assert gitlab_issue.description != jira_issue.description

    gitlab_issue, jira_issue = rule.sync(gitlab_issue, jira_issue)

    assert gitlab_issue.description == jira_issue.description


def test_src_to_dest_sync():
    db = MockDatabase()
    issues_svc: IssuesService = IssuesService(db)

    src: RuleSide = RuleSide(
        tracker="gitlab",
        project="KAN",
        field="description",
    )

    dest: RuleSide = RuleSide(
        tracker="jira",
        project="KAN",
        field="description",
    )

    rule = Rule(
        source=src,
        destination=dest,
        condition=FieldEqualityCondition(direction=RuleDirection.SRC_TO_DEST),
    )

    issues = issues_svc.get_issues()
    gitlab_issue: Issue = [x for x in issues if x.issue_name == "hello world"][0]
    jira_issue: Issue = [x for x in issues if x.issue_name == "hello world"][1]

    assert gitlab_issue.description != jira_issue.description

    gitlab_issue, jira_issue = rule.sync(gitlab_issue, jira_issue)

    assert gitlab_issue.description == jira_issue.description


def test_dest_to_src_sync():
    db = MockDatabase()
    issues_svc: IssuesService = IssuesService(db)

    src: RuleSide = RuleSide(
        tracker="gitlab",
        project="KAN",
        field="description",
    )

    dest: RuleSide = RuleSide(
        tracker="jira",
        project="KAN",
        field="description",
    )

    rule = Rule(
        source=src,
        destination=dest,
        condition=FieldEqualityCondition(direction=RuleDirection.DEST_TO_SRC),
    )

    issues = issues_svc.get_issues()
    gitlab_issue: Issue = [x for x in issues if x.issue_name == "hello world"][0]
    jira_issue: Issue = [x for x in issues if x.issue_name == "hello world"][1]

    assert gitlab_issue.description != jira_issue.description

    gitlab_issue, jira_issue = rule.sync(gitlab_issue, jira_issue)

    assert gitlab_issue.description == jira_issue.description
