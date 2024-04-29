from app.core.providers import get_provider
from app.core.issues import DEFAULT_ATTRS_MAP
import pytest

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
        return text + text if len(text) < 16 else "text"

    issues = provider.get_project_issues(BAORD_NAME)

    assert len(issues) != 0, "Issues must not be empty"

    issue_description_map = {
        issue.issue_id: issue.description for issue in issues
    }

    for issue in issues:
        data = {"description": get_description(issue.description)}
        issue.import_values(data)
        issue.update()

    issues = provider.get_project_issues(BAORD_NAME)

    assert len(issues) != 0, "Issues must not be empty"

    for issue in issues:
        assert (
            issue.description != issue_description_map[issue.issue_id]
        ), "Failed to update issue"
