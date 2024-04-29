from app.core.db import Database
from app.core.issues import Issue


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
