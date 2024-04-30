from app.core.db import Database
from app.core.issues import Issue
from app.core.providers import Provider
from app.core.logger import logger
from typing import Optional


class IssuesService:
    def __init__(self, db: Database):
        self._db: Database = db

    # TODO: add providers
    def get_issues(self) -> list[Issue]:
        issues_dicts: list[dict] = self._db.get_all("issues")
        print(issues_dicts)
        issues: list[Issue] = []

        for issue_dict in issues_dicts:
            issue = Issue()
            issue.import_values(issue_dict)
            issues.append(issue)

        return issues

    def get_related_issue(
        self, issue: Issue, target_project_name: str, target_provider: Provider
    ) -> Optional[Issue]:
        # TODO: fetch from db if possible
        # TODO: change to ids
        logger.debug(
            f"fetching related issue: t_project: {target_project_name}")
        related_issue: Optional[Issue] = target_provider.get_project_issue_by_name(
            target_project_name, issue.issue_name
        )
        return related_issue

        # TODO: save to DB
