from app.core.db import DocumentDatabase, MockDatabase
from typing import List, Dict
import pytest


@pytest.fixture
def init_document_db() -> DocumentDatabase:
    db = DocumentDatabase(":memory:")
    return db

@pytest.mark.unit
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

@pytest.mark.unit
def test_document_db_add_multiple_rows_rowwise(
    init_document_db: DocumentDatabase,
):
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


@pytest.mark.unit
def test_document_db_add_all_rows(init_document_db: DocumentDatabase):
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


@pytest.mark.unit
def test_document_db_find(init_document_db: DocumentDatabase):
    """
    Test adding multiple rows to the database in bulk and then finding
    """
    db = init_document_db
    issues: List[Dict] = MockDatabase.prepare_mock_issues()
    db.add_all("issues", issues)
    db_found_issues = db.find("issues", issues[0])

    length = len(db_found_issues)
    assert length == 1, f"Expected 1 found issue, found: {length}"

    db_issue = db_found_issues[0]

    for key, value in issues[0].items():
        assert key in db_issue, f"Key {key} not found in db issue"

        assert (
            value == db_issue[key]
        ), f"Value mismatch for {key}: expected {value}, got {db_issue[key]}"
