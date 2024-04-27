from typing import Dict, List
from dacite import from_dict
from app.core.issues import GitlabIssue, JiraIssue, Issue, DefaultSource
from abc import ABC
from typing import Optional, Any
from gitlab.v4.objects.issues import ProjectIssue as _GitlabIssue
from jira import Issue as _JiraIssue


class Database(ABC):
    # TODO: https://pypi.org/project/pyejdb/
    def get(self, key: str) -> Optional[Any]:
        pass


def prepare_mock_issues() -> List[Dict]:
    issues: List[Dict] = []

    gl_source = DefaultSource(
        issue_id="1",
        issue_name="hello world",
        created_at="2024-04-27T10:15:30.123456+0530",
        updated_at="2024-04-27T10:15:30.123456+0530",
        description="default issue old",
    )

    jr_source = DefaultSource(
        issue_id="2",
        issue_name="hello world",
        created_at="2024-04-28T10:15:30.123456+0530",
        updated_at="2024-04-28T10:15:30.123456+0530",
        description="default issue new",
    )

    gl_issue = Issue(gl_source)
    jr_issue = Issue(jr_source)

    print(gl_issue.asdict())

    issues.append(gl_issue.asdict())
    issues.append(jr_issue.asdict())

    return issues


class MockDatabase(Database):
    def __init__(self):
        self._db = {"issues": prepare_mock_issues()}

    def get(self, key: str) -> Optional[Any]:
        return self._db.get(key, None)