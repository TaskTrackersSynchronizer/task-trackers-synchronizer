from app.core.db import Database
from app.core.issues import Issue
from typing import List, Dict
from dacite import from_dict
from dataclasses import asdict


class IssuesService:
    def __init__(self, db: Database):
        self._db: Database = db

    # TODO: add providers
    def get_issues(self) -> List[Issue]:
        issues_dicts: List[Dict] = self._db.get("issues")
        issues: List[Issue] = []
        print(issues_dicts)
        for issue_dict in issues_dicts:
            issue = Issue()
            issue.import_values(issue_dict)
            issues.append(issue)

        return issues
