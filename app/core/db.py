from app.core.issues import Issue, DefaultSource
from abc import ABC, abstractmethod
from functools import reduce
from copy import deepcopy

import sqlite3
import json
import typing as t


class Database(ABC):
    """
    Abstract class for database connections
    """

    @abstractmethod
    def get_all(self, table_name: str) -> list[dict]:
        pass

    @abstractmethod
    def add_row(self, table_name: str, row: dict) -> None:
        pass

    @abstractmethod
    def add_all(self, table_name: str, rows: list[dict]) -> None:
        pass

    @abstractmethod
    def find(self, table_name: str, query: dict) -> list[dict]:
        pass

    @abstractmethod
    def close(self):
        pass


class DocumentDatabase(Database):
    """
    Database class for storing documents in a SQLite database in a
    NoSQL-like way
    """

    # A list of allowed tables. Tables with such names will be created
    # if they don't exist in the DB.
    TABLES: dict[str, str] = {
        "issues": "issues",
        "rules": "rules",
    }

    def __init__(self, f: str):
        """
        Create a new database connection
        :param f: path to the database file
        """
        self._db = sqlite3.connect(f)
        for table_name in self.TABLES.keys():
            query = f"CREATE TABLE IF NOT EXISTS {table_name} (data TEXT);"
            self._db.execute(query)

    def _check_table(self, table_name: str) -> None:
        """
        Check if table exists, otherwise raise a KeyError
        :param table_name: name of the table
        :return: True if table exists, False otherwise
        """
        if table_name not in self.TABLES:
            raise KeyError(f"Table {table_name} not found")

    def _execute(self, query) -> t.Any:
        """
        Execute a query
        :param query: SQL query
        return: result of the query
        """
        return self._db.execute(query)

    def add_row(self, table_name: str, row: dict) -> None:
        """
        Add a row to a table
        :param table_name: name of the table
        :param row: dictionary representing the row
        """
        self._check_table(table_name)
        query = f"INSERT INTO {table_name} VALUES (?);"
        self._db.execute(query, (json.dumps(row),))

    def add_all(self, table_name: str, rows: list[dict]) -> None:
        """
        Add multiple rows to a table
        :param table_name: name of the table
        :param rows: list of dictionaries representing the rows
        """
        self._check_table(table_name)
        for row in rows:
            self.add_row(table_name, row)

    def get_all(self, table_name: str) -> list[dict]:
        """
        Get all rows from a table
        :param table_name: name of the table
        :return: list of dictionaries representing the rows in the table
        """
        self._check_table(table_name)
        results = []
        for r in self._db.execute(f"SELECT * FROM {table_name}"):
            results.append(json.loads(r[0]))
        return results

    def find(self, table_name: str, query: dict) -> list[dict]:
        """
        Find rows in a table that match a query
        Limitations: only supports exact matches
                     (check dict elements for equality)
        :param table: name of the table
        :param query: dictionary of key-value pairs to match
        :return: list of dictionaries representing the rows that
                 match the query (empty if none match)
        """

        def accum_func(
            accumulator: list[str], query_row: tuple[str, object]
        ) -> list[object]:
            return accumulator + [f"$.{query_row[0]}", query_row[1]]

        results = []

        q = " AND ".join([" json_extract(data, ?) = ?"] * len(query))

        statement = self._db.execute(
            f"SELECT * FROM {table_name} WHERE {q}",
            reduce(accum_func, query.items(), []),
        )

        for r in statement:
            # we need generators here? do yield then instead of adding
            # to the list
            # yield r[0]
            results.append(json.loads(r[0]))

        return results

    def close(self):
        """
        Close the database connection
        """
        try:
            # check if connection is still open
            self._execute("SELECT 1")
            self._db.close()
        except sqlite3.ProgrammingError:
            pass  # connection is already closed

    def __del__(self):
        """
        Destructor closing the database connection if needed.
        """
        self.close()


class MockDatabase(Database):
    def __init__(self):
        self._db = {"issues": self.prepare_mock_issues()}

    def get_all(self, table_name: str = "issues") -> list[dict]:
        return [deepcopy(x) for x in self._db[table_name]]

    def add_row(self, table_name: str, row: dict) -> None:
        raise NotImplementedError()

    def add_all(self, table_name: str, rows: list[dict]) -> None:
        raise NotImplementedError()

    def find(self, table_name: str, query: dict) -> list[dict]:
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()

    @staticmethod
    def prepare_mock_issues() -> list[dict]:
        issues: list[dict] = []

        gl_source = DefaultSource(
            issue_id="1",
            issue_name="hello world",
            created_at="2024-04-27T10:15:30.123456+0530",
            updated_at="2024-04-27T10:15:30.123456+0530",
            description="default issue old",
        )

        jr_source = DefaultSource(
            issue_id="2",
            issue_name="hello world",
            created_at="2024-04-28T10:15:30.123456+0530",
            updated_at="2024-04-28T10:15:30.123456+0530",
            description="default issue new",
        )

        gl_issue = Issue(gl_source)
        jr_issue = Issue(jr_source)

        issues.append(gl_issue.asdict())
        issues.append(jr_issue.asdict())

        return issues
