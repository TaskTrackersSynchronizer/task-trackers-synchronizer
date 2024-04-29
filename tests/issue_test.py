from app.core.providers import Provider, get_provider, PROVIDER_NAMES
from app.core.issues import DEFAULT_ATTRS_MAP
import pytest
from datetime import datetime

BOARD_NAME = "KAN"


@pytest.mark.integration
@pytest.mark.parametrize("provider", PROVIDER_NAMES)
def test_issue_creation(provider):
    provider = get_provider(provider)
    issues = provider.get_project_issues(BOARD_NAME)

    assert len(issues) != 0, "Issues must not be empty"

    for issue in issues:
        for attr in DEFAULT_ATTRS_MAP:
            assert hasattr(issue, attr), f"No attr {attr} found"


@pytest.mark.integration
@pytest.mark.parametrize("provider", PROVIDER_NAMES)
def test_issue_update(provider):
    provider = get_provider(provider)

    def get_description(text: str) -> str:
        return text + text if len(text) < 16 else "text"

    issues = provider.get_project_issues(BOARD_NAME)

    assert len(issues) != 0, "Issues must not be empty"

    issue_description_map = {
        issue.issue_id: issue.description for issue in issues
    }

    for issue in issues:
        data = {"description": get_description(issue.description)}
        issue.import_values(data)
        issue.update()

    issues = provider.get_project_issues(BOARD_NAME)

    assert len(issues) != 0, "Issues must not be empty"

    for issue in issues:
        assert (
            issue.description != issue_description_map[issue.issue_id]
        ), "Failed to update issue"


@pytest.mark.integration
def test_jira_get_last_updated_at():
    provider: Provider = get_provider("jira")

    updated_at_str = "2021-04-28T10:15:30.123456+0530"
    updated_at = datetime.strptime(updated_at_str, "%Y-%m-%dT%H:%M:%S.%f%z")

    issues = provider.get_last_updated_issues(updated_at)

    print(f"issues: {issues} size: {len(issues)}")


@pytest.mark.integration
def test_gitlab_get_last_updated_at():
    provider: Provider = get_provider("gitlab")

    updated_at_str = "2021-04-28T10:15:30.123456+0530"
    updated_at = datetime.strptime(updated_at_str, "%Y-%m-%dT%H:%M:%S.%f%z")

    issues = provider.get_last_updated_issues(updated_at)

    print(f"issues: {issues} size: {len(issues)}")
