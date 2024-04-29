from app.core.providers import get_provider, JiraProvider
from app.core.issues import DEFAULT_ATTRS_MAP, GitlabIssue, JiraIssue
import pytest
from datetime import datetime

BAORD_NAME = "KAN"
PROVIDERS = [get_provider("jira"), get_provider("gitlab")]


@pytest.mark.parametrize("provider", PROVIDERS)
def test_issue_creation(provider):
    issues = provider.get_project_issues(BAORD_NAME)

    assert len(issues) != 0, "Issues must not be empty"

    for issue in issues:
        for attr in DEFAULT_ATTRS_MAP:
            assert hasattr(issue, attr), f"No attr {attr} found"


@pytest.mark.parametrize("provider", PROVIDERS)
def test_issue_update(provider):
    def get_description(text: str) -> str:
        now = datetime.now()
        formatted = now.strftime("%Y-%m-%d %H:%M:%S")
        return f"test_{formatted}"

    issues = provider.get_project_issues(BAORD_NAME)

    assert len(issues) != 0, "Issues must not be empty"

    issue_description_map = {issue.issue_id: issue.description for issue in issues}

    for issue in issues:
        # TODO: assert on new values

        data = {"description": get_description(issue.description)}
        issue.import_values(data)
        issue.update()

    issues = provider.get_project_issues(BAORD_NAME)

    assert len(issues) != 0, "Issues must not be empty"

    for issue in issues:
        assert (
            issue.description != issue_description_map[issue.issue_id]
        ), "Failed to update issue"


def test_jira_get_last_updated_at():
    provider: JiraProvider = get_provider("jira")
    last_updated = ""

    updated_at_str = "2021-04-28T10:15:30.123456+0530"
    updated_at = datetime.strptime(updated_at_str, "%Y-%m-%dT%H:%M:%S.%f%z")

    # print(tmp)

    issues = provider.get_last_updated_issues(updated_at)

    print(f"issues: {issues} size: {len(issues)}")


def test_gitlab_get_last_updated_at():
    provider: GitlabProvider = get_provider("gitlab")

    updated_at_str = "2021-04-28T10:15:30.123456+0530"
    updated_at = datetime.strptime(updated_at_str, "%Y-%m-%dT%H:%M:%S.%f%z")

    issues = provider.get_last_updated_issues(updated_at)

    print(f"issues: {issues} size: {len(issues)}")

    # updated_at: str = "2024-04-27 05:01:16"


def test_gitlab_get_issue_by_name():
    provider: GitlabProvider = get_provider("gitlab")

    issue = provider.get_project_issue_by_name("KAN", "name")
    assert issue is not None
    assert gitlab_issue.issue_name == "name"


def test_jira_get_issue_by_name():
    provider: JiraProvider = get_provider("jira")

    issue = provider.get_project_issue_by_name("KAN", "name")
    assert issue is not None
    assert issue.issue_name == "name"
