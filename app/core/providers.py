from abc import ABC, abstractmethod
from gitlab import Gitlab, GitlabError
from jira import JIRA, JIRAError
from dotenv import load_dotenv

from issues import Issue, JiraIssue, GitlabIssue

import re
import os

load_dotenv()

JIRA_SERVER = os.environ.get("JIRA_SERVER", "")
JIRA_EMAIL = os.environ.get("JIRA_EMAIL", "")
JIRA_PAT = os.environ.get("JIRA_PAT", "")

GITLAB_SERVER = os.environ.get("GITLAB_SERVER", "")
GITLAB_PAT = os.environ.get("GITLAB_PAT", "")


class Provider(ABC):
    @abstractmethod
    def get_project_issues(self, project_name: str) -> list[Issue]:
        pass


class GitlabProvider(Provider):
    def __init__(self) -> None:
        self._client = Gitlab(url=GITLAB_SERVER, oauth_token=GITLAB_PAT)
        self._client.auth()

        self._user_id = self._client.user.id
        self._user = self._client.users.get(self._user_id)

    def get_project_issues(self, project_name: str) -> list[GitlabIssue]:
        user_projects = self._user.projects.list(pagination=False)
        user_project = next(filter(lambda x: x.name == project_name, user_projects))

        if not user_project:
            raise GitlabError("Gitlab project not found")

        project = self._client.projects.get(user_project.id)
        issues = project.issues.list(pagination=False)
        return list(map(GitlabIssue, issues))


class JiraProvider(Provider):
    def __init__(self) -> None:
        self._client = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_EMAIL, JIRA_PAT))

    def get_project_issues(self, project_name: str) -> list[JiraIssue]:
        # validate project name
        if not re.fullmatch(r"\w{2,80}", project_name):
            raise JIRAError("Invalid project name")

        # TODO: handle query injection attacks more accurate
        issues = self._client.search_issues(f"project = {project_name}")
        return list(map(JiraIssue, issues))


if __name__ == "__main__":
    gitlab_provider = GitlabProvider()
    jira_provider = JiraProvider()

    data = {"description": "NEW1"}

    gitlab_issue = gitlab_provider.get_project_issues("KAN")[0]
    gitlab_issue.import_values(data)
    gitlab_issue.update()

    jira_issue = jira_provider.get_project_issues("KAN")[0]
    jira_issue.import_values(data)
    jira_issue.update()

    print(gitlab_issue.asdict())
    print(jira_issue.asdict())
