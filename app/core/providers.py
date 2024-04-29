from abc import ABC, abstractmethod
from gitlab import Gitlab, GitlabError
from jira import JIRA, JIRAError
from dotenv import load_dotenv

from app.core.issues import Issue, JiraIssue, GitlabIssue

import typing as t
import re
import os

load_dotenv()

# mock default creds are used. TODO: parametrize
JIRA_SERVER = os.environ.get("JIRA_SERVER", "https://0xf1o2732.atlassian.net")
JIRA_EMAIL = os.environ.get("JIRA_EMAIL", "0xf1o2732@proton.me")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN", "")

GITLAB_SERVER = os.environ.get("GITLAB_SERVER", "https://gitlab.com")
GITLAB_API_TOKEN = os.environ.get("GITLAB_API_TOKEN", "")


class Provider(ABC):
    @abstractmethod
    def get_project_issues(self, project_name: str) -> list[Issue]:
        pass


class GitlabProvider(Provider):
    def __init__(self) -> None:
        self._client = Gitlab(url=GITLAB_SERVER, oauth_token=GITLAB_API_TOKEN)
        self._client.auth()

        self._user_id = self._client.user.id
        self._user = self._client.users.get(self._user_id)

    def get_project_issues(self, project_name: str) -> list[GitlabIssue]:
        user_projects = self._user.projects.list(pagination=False)
        user_project = next(
            filter(lambda x: x.name == project_name, user_projects)
        )

        if not user_project:
            raise GitlabError("Gitlab project not found")

        project = self._client.projects.get(user_project.id)
        issues = project.issues.list(pagination=False)
        return list(map(GitlabIssue, issues))


class JiraProvider(Provider):
    def __init__(self) -> None:
        self._client = JIRA(
            server=JIRA_SERVER, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN)
        )

    def get_project_issues(self, project_name: str) -> list[JiraIssue]:
        # validate project name
        if not re.fullmatch(r"\w{2,80}", project_name):
            raise JIRAError("Invalid project name")

        # TODO: handle query injection attacks more accurate
        issues = self._client.search_issues(f'project = "{project_name}"')
        return list(map(JiraIssue, issues))


PROVIDERS = {
    "gitlab": GitlabProvider(),
    "jira": JiraProvider(),
}


def get_provider(name: str) -> t.Optional[Provider]:
    return PROVIDERS.get(name, None)
