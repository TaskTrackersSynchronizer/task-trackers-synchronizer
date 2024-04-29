from app.services.syncer import Syncer
from app.core.providers import JiraProvider, GitlabProvider
from app.core.issues import Issue, JiraIssue, GitlabIssue, IssuePair
from app.core.db import MockDatabase
from app.core.providers import get_provider


# def test_syncs_existing():
#     # TODO: backup all existing
#     db = MockDatabase()
#     syncer: Syncer = Syncer(db)

#     jira_provider = get_provider("jira")
#     gitlab_provider = get_provider("gitlab")

#     jira_issues: list[JiraIssue] = jira_provider.get_issues("")
#     gitlab_issues: list[GitlabIssue] = gitlab_provider.get_issues("")

#     related_issues: list[IssuePair] = Issue.filter_related(
#         jira_issues, gitlab_issues
#     )
#     unsynced_issues = [x for x in related_issues if not x.src.is_synced(x.dst)]

#     assert len(unsynced_issues) > 0

#     syncer.sync_all()

#     jira_issues: list[JiraIssue] = jira_provider.get_issues()
#     gitlab_issues: list[GitlabIssue] = gitlab_provider.get_issues()

#     related_issues: list[IssuePair] = Issue.filter_related(
#         jira_issues, gitlab_issues
#     )
#     unsynced_issues = [x for x in related_issues if not x.src.is_synced(x.dst)]

#     assert len(unsynced_issues) == 0

    # 1. get all gitlab&jira issues (optionally older than specified timestamp)
    # 2. assert that some fields are not equal
    # 3. call sync_all
    # 4. assert that fields are synced
    # 5. import old values to the issues
    # 6. update issues to contain old values


def test_sync_minimal():
    gitlab_provider = GitlabProvider()
    jira_provider = JiraProvider()

    syncer = Syncer(MockDatabase())

    data0 = {"issue_name": "name", "description": "NEW0"}
    data1 = {"issue_name": "name", "description": "NEW1"}

    gitlab_issue = gitlab_provider.get_project_issues("KAN")[0]
    gitlab_issue.import_values(data0)
    gitlab_issue.update()

    jira_issue = jira_provider.get_project_issues("KAN")[0]
    jira_issue.import_values(data1)
    jira_issue.update()

    src_issues = gitlab_provider.get_project_issues("KAN")
    dst_issues = jira_provider.get_project_issues("KAN")

    syncer.sync_minimal(src_issues, dst_issues)
    
    assert all(
        x.description == y.description
        for x in src_issues
        for y in dst_issues
    )
