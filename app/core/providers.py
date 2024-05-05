from abc import ABC, abstractmethod
from gitlab import Gitlab, GitlabError
from gitlab.v4.objects.projects import Project as _GitlabProject
from jira import JIRA, JIRAError
from dotenv import load_dotenv
from datetime import datetime
import pytest
from app.core.logger import logger
from app.core.project import Project
from app.core.issues import Issue, JiraIssue, GitlabIssue, DEFAULT_EXCLUDE_FIELDS

import typing as t
import re
import os
from typing import Optional
from copy import deepcopy

load_dotenv()

# mock default creds are used. TODO: parametrize
JIRA_SERVER = os.environ.get("JIRA_SERVER", "https://0xf1o2732.atlassian.net")
JIRA_EMAIL = os.environ.get("JIRA_EMAIL", "0xf1o2732@proton.me")
GITLAB_SERVER = os.environ.get("GITLAB_SERVER", "https://gitlab.com")


class Provider(ABC):
    @abstractmethod
    def get_projects(
        self,
    ) -> list[Project]:
        pass

    @abstractmethod
    def get_project_issues(
        self, project_name: str, updated_at: Optional[datetime] = None
    ) -> list[Issue]:
        pass

    @abstractmethod
    def get_last_updated_issues(self, updated_at: datetime) -> list[Issue]:
        pass

    @abstractmethod
    def get_project_issue_by_name(
        self, project_name: str, issue_name: str
    ) -> Optional[Issue]:
        pass

    @abstractmethod
    def create_issue(self, project_name: str, issue_name: str) -> Issue:
        pass


@pytest.mark.integration
class GitlabProvider(Provider):
    def __init__(self) -> None:
        GITLAB_API_TOKEN = os.environ.get("GITLAB_API_TOKEN", "")
        assert GITLAB_API_TOKEN, "GITLAB_API_TOKEN is not set"
        self._client = Gitlab(url=GITLAB_SERVER, oauth_token=GITLAB_API_TOKEN)
        self._client.auth()

        self._user_id = self._client.user.id
        self._issues_api = self._client.issues
        self._user = self._client.users.get(self._user_id)

    def _get_project(self, project_name: str) -> _GitlabProject:
        user_projects = self._user.projects.list(pagination=False)
        user_project = next(filter(lambda x: x.name == project_name, user_projects))

        if not user_project:
            raise GitlabError("Gitlab project not found")

        return self._client.projects.get(user_project.id)

    def get_projects(self) -> list[Project]:
        user_projects = self._user.projects.list(pagination=False)
        return [
            Project(name=x.name, project_id=x.id, provider="Gitlab")
            for x in user_projects
        ]

    def get_project_issues(
        self, project_name: str, updated_at: Optional[datetime] = None
    ) -> list[GitlabIssue]:
        project = self._get_project(project_name)

        if updated_at is not None:
            issues = project.issues.list(pagination=False, updated_after=updated_at)
        else:
            issues = project.issues.list(pagination=False)

        if len(issues) == 0:
            return []
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

    def get_project_issue_by_name(
        self, project_name: str, issue_name: str
    ) -> Optional[Issue]:
        user_projects = self._user.projects.list(pagination=False)
        user_project = next(filter(lambda x: x.name == project_name, user_projects))

        if not user_project:
            raise GitlabError("Gitlab project not found")

        project = self._client.projects.get(user_project.id)
        issue = project.issues.list(
            pagination=False,
            title=issue_name,
            order_by="created_at",
            sort="asc",
        )

        print(issue)

        if isinstance(issue, list):
            if len(issue) > 0:
                return GitlabIssue(issue[0])
            return None
        elif issue:
            return GitlabIssue(issue)
        else:
            return None

    def create_issue(self, project_name: str, issue_name: str) -> GitlabIssue:
        project = self._get_project(project_name)

        values = {}
        values["title"] = issue_name

        issue = project.issues.create(values)
        return GitlabIssue(issue)


class JiraProvider(Provider):
    def __init__(self) -> None:
        JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN", "")
        assert JIRA_API_TOKEN, "JIRA_API_TOKEN is not set"
        self._client = JIRA(server=JIRA_SERVER, basic_auth=(JIRA_EMAIL, JIRA_API_TOKEN))

    def get_projects(self) -> list[Project]:
        projects = self._client.projects()
        return [Project(name=x.key, project_id=x.id, tracker="Jira") for x in projects]

    def _get_issues_by_query(self, query: str) -> list[JiraIssue]:
        issues = self._client.search_issues(query)
        return list(map(JiraIssue, issues))

    def get_project_issue_by_name(
        self, project_name: str, issue_name: str
    ) -> Optional[Issue]:
        issues = self._get_issues_by_query(
            f'project = "{project_name}" AND summary ~ "{issue_name}"'
        )
        logger.debug(issues)
        if isinstance(issues, list):
            if len(issues) > 0:
                return issues[0]
            return None
        return issues

    # todo: allow fetching from list of projects
    def get_project_issues(
        self, project_name: str, updated_at: Optional[datetime] = None
    ) -> list[JiraIssue]:
        # validate project name
        if not re.fullmatch(r"\w{2,80}", project_name):
            raise JIRAError("Invalid project name")

        query = f'project = "{project_name}"'
        if updated_at is not None:
            updated_at_str = updated_at.strftime("%Y-%m-%d %H:%M")
            query += f" AND updated >= '{updated_at_str}'"
        issues = self._get_issues_by_query(query)
        return issues

    def get_last_updated_issues(
        self, updated_at: datetime = datetime.fromtimestamp(0)
    ) -> list[JiraIssue]:
        updated_at_str = updated_at.strftime("%Y-%m-%d %H:%M")

        return self._get_issues_by_query(f"updated>='{updated_at_str}'")

    def create_issue(self, project_name: str, issue_name: str) -> Issue:
        values = {}
        values["project"] = {"key": project_name}
        values["issuetype"] = {"name": "Task"}
        values["summary"] = issue_name
        issue = self._client.create_issue(values)
        return JiraIssue(issue)


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
    "jira": SingletonObject(JiraProvider),
}
PROVIDER_NAMES = list(PROVIDERS_OBJS.keys())


def get_provider(provider_name: str) -> Provider:
    return PROVIDERS_OBJS[provider_name.lower()].get_instance()
