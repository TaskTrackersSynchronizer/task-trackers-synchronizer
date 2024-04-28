from app.core.db import DocumentDatabase, MockDatabase
from app.services.issues import Issue
from typing import List, Dict
import pytest


@pytest.fixture
def init_document_db() -> DocumentDatabase:
    db = DocumentDatabase(":memory:")
    return db


def test_document_db_add_single_row(init_document_db: DocumentDatabase):
    """
    Test adding a single row to the database
    """
    db = init_document_db
    issue = MockDatabase.prepare_mock_issues()[0]
    db.add_row("issues", issue)
    db_stored_issues = db.get_all("issues")
    assert len(db_stored_issues) == 1, "Unexpected number of rows in the table"
    assert db_stored_issues[0] == issue, "DB and original issues do not match"


def test_document_db_add_multiple_rows_rowwise(init_document_db: DocumentDatabase):
    """
    Test adding a single row to the database
    """
    db = init_document_db
    issues: List[Dict] = MockDatabase.prepare_mock_issues()
    for issue_row in issues:
        db.add_row("issues", issue_row)
    db_stored_issues = db.get_all("issues")
    assert len(db_stored_issues) == len(
        issues
    ), "Unexpected number of rows in the table"
    assert (
        db_issue == issue for db_issue, issue in zip(db_stored_issues, issues)
    ), "DB and original issues do not match"


def test_document_db_add_multiple_rows_bulk(init_document_db: DocumentDatabase):
    """
    Test adding multiple rows to the database in bulk
    """
    db = init_document_db
    issues: List[Dict] = MockDatabase.prepare_mock_issues()
    db.add_all("issues", issues)
    db_stored_issues = db.get_all("issues")
    assert len(db_stored_issues) == len(
        issues
    ), "Unexpected number of rows in the table"
    assert (
        db_issue == issue for db_issue, issue in zip(db_stored_issues, issues)
    ), "DB and original issues do not match"