from gitlab.v4.objects.issues import ProjectIssue as _GitlabIssue
from jira import Issue as _JiraIssue
from dataclasses import dataclass


@dataclass
class Issue:
    issue_id: str
    issue_name: str
    issue_type: str
    created_at: str
    updated_at: str
    description: str

    def asdict(self) -> dict[str, str]:
        return {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith("_")
            and not callable(value)
            and not callable(getattr(value, "__get__", None))
        }


class GitlabIssue(Issue):
    def __init__(self, source_issue: _GitlabIssue) -> None:
        self._source_issue = source_issue

        super().__init__(
            str(source_issue.iid),
            source_issue.title,
            source_issue.issue_type,
            source_issue.created_at,
            source_issue.updated_at,
            source_issue.description,
        )


class JiraIssue(Issue):
    def __init__(self, source_issue: _JiraIssue) -> None:
        self._source_issue = source_issue

        super().__init__(
            source_issue.id,
            source_issue.fields.summary,
            source_issue.fields.issuetype.name.lower(),
            source_issue.fields.created,
            source_issue.fields.updated,
            str(source_issue.fields.description),
        )

    def asdict(self) -> dict[str, str]:
        return super().asdict()
