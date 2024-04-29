from abc import ABC, abstractmethod
from gitlab import Gitlab, GitlabError
from jira import JIRA, JIRAError
from dotenv import load_dotenv
from datetime import datetime
import pytest

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

    @abstractmethod
    def get_last_updated_issues(self, updated_at: datetime) -> list[Issue]:
        pass


@pytest.mark.integration
class GitlabProvider(Provider):
    def __init__(self) -> None:
        self._client = Gitlab(url=GITLAB_SERVER, oauth_token=GITLAB_API_TOKEN)
        self._client.auth()

        self._user_id = self._client.user.id
        self._issues_api = self._client.issues
        self._user = self._client.users.get(self._user_id)

    def get_project_issues(self, project_name: str) -> list[GitlabIssue]:
        user_projects = self._user.projects.list(pagination=False)
        user_project = filter(lambda x: x.name == project_name, user_projects)

        if not user_project:
            raise GitlabError("Gitlab project not found")

        project = self._client.projects.get(user_project.id)
        issues = project.issues.list(pagination=False)
        return list(map(GitlabIssue, issues))

    def get_last_updated_issues(
        self, updated_at: datetime = datetime.fromtimestamp(0)
    ) -> list[GitlabIssue]:
        user_projects = self._user.projects.list(pagination=False)
        issues: list[GitlabIssue] = []
        for project in user_projects:
            project = self._client.projects.get(project.id)
            updated_at_str = datetime.isoformat(updated_at)
            project_issues = project.issues.list(
                pagination=False, updated_after=updated_at_str
            )
            issues += project_issues

        return list(map(GitlabIssue, issues))

    def get_issues(self, query: str = "") -> list[GitlabIssue]:
        # TODO: refactor this shit somebody if you care
        return self.get_last_updated_issues()


class JiraProvider(Provider):
    def __init__(self) -> None:
        self._client = JIRA(
            server=JIRA_SERVER, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN)
        )

    def get_issues(self, query: str = "") -> list[JiraIssue]:
        issues = self._client.search_issues(query)
        return list(map(JiraIssue, issues))

    # todo: allow fetching from list of projects
    def get_project_issues(self, project_name: str) -> list[JiraIssue]:
        # validate project name
        if not re.fullmatch(r"\w{2,80}", project_name):
            raise JIRAError("Invalid project name")

        # TODO: handle query injection attacks more accurate
        issues = self.get_issues(f'project = "{project_name}"')
        return issues

    def get_last_updated_issues(self, updated_at: datetime) -> list[JiraIssue]:
        updated_at_str = updated_at.strftime("%Y-%m-%d %H:%M")

        return self.get_issues(f"updated>='{updated_at_str}'")


class SingletonObject:
    def __init__(self, wrapped_class, *args, **kwargs):
        self._cls = wrapped_class
        self._args = args
        self._kwargs = kwargs
        self._instance = None

    def get_instance(self):
        if self._instance is None:
            self._instance = self._cls(*self._args, **self._kwargs)
        return self._instance


PROVIDERS_OBJS: t.Dict = {
    "gitlab": SingletonObject(GitlabProvider),
    "jira": SingletonObject(JiraProvider)
}
PROVIDER_NAMES = list(PROVIDERS_OBJS.keys())


def get_provider(provider_name: str) -> Provider:
    return PROVIDERS_OBJS[provider_name].get_instance()
