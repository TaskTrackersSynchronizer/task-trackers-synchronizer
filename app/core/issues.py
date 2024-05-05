from gitlab.v4.objects.issues import ProjectIssue as _GitlabIssue
from jira import Issue as _JiraIssue
from dataclasses import dataclass, field
from datetime import datetime
from functools import reduce
from collections import defaultdict

import typing as t

_T = t.TypeVar("_T", bound=object)


@dataclass
class ConvertableAttr:
    attr: str
    convert: t.Callable[[_T], str] = field(default=lambda x: str(x))
    unconvert: t.Callable[[str], _T] = field(default=lambda x: str(x))

    def resolve_value(self, obj: object) -> _T:
        return reduce(getattr, [obj] + self.attr.split("."))

    def resolve_type(self, obj: object) -> t.Type:
        return type(self.resolve_value(obj))

    def set_value(
        self,
        obj: object,
        value: object,
        unconvert: bool = True,
    ) -> None:
        attr_split = self.attr.split(".")
        attr_chain, attr_last = attr_split[:-1], attr_split[-1]
        obj_last = reduce(getattr, [obj] + attr_chain)

        value_c = self.unconvert(value) if unconvert else value
        setattr(obj_last, attr_last, value_c)


DEFAULT_ATTRS_MAP = {
    "issue_id": ConvertableAttr("issue_id"),
    "issue_name": ConvertableAttr("issue_name"),
    "created_at": ConvertableAttr("created_at"),
    "updated_at": ConvertableAttr("updated_at"),
    "description": ConvertableAttr("description"),
}


DEFAULT_EXCLUDE_FIELDS = ["issue_id", "created_at", "updated_at"]


@dataclass
class DefaultSource:
    issue_id: str = "1"
    issue_name: str = "hello world"
    created_at: str = "2024-04-26 05:01:16"
    updated_at: str = "2024-04-27 05:01:16"
    description: str = "default issue"


@dataclass
class Issue:
    _default_attrs = {
        "issue_id",
        "issue_name",
        "created_at",
        "updated_at",
        "description",
    }

    def __init__(
        self,
        source: object = DefaultSource(),
        attrs_map: dict[str, ConvertableAttr] = DEFAULT_ATTRS_MAP,
    ) -> None:
        self._source = source

        if not all(key in attrs_map.keys() for key in self._default_attrs):
            raise ValueError("attrs_map is incomplete")

        self._attrs_map = attrs_map

        for key in attrs_map:
            c_attr = self._attrs_map[key]
            setattr(
                self, key, c_attr.convert(c_attr.resolve_value(self._source))
            )

    def asdict(self) -> dict[str, str]:
        return {
            key: value
            for key, value in self.__dict__.items()
            if not key.startswith("_")
            and not callable(value)
            and not callable(getattr(value, "__get__", None))
        }

    @staticmethod
    def filter_related(
        src_issues: list["Issue"], dst_issues: list["Issue"]
    ) -> list["IssuePair"]:
        issue_name_map: dict[str, list["Issue"]] = defaultdict(
            lambda: [None, None],
        )

        for src_issue in src_issues:
            issue_name_map[src_issue.issue_name][0] = src_issue

        for dst_issue in dst_issues:
            issue_name_map[dst_issue.issue_name][1] = dst_issue

        related_pairs: list["IssuePair"] = [
            IssuePair(x[0], x[1]) for x in issue_name_map.values()
        ]

        return related_pairs

    @property
    def id_field(self) -> str:
        return "issue_name"

    def is_synced(self, other: "Issue") -> bool:
        if other is None:
            return False

        try:
            other_values = other.export_values(unconvert=False)
            for f, value in self.export_values(unconvert=False).items():
                if other_values[f] != value:
                    return False
            return True
        except Exception:
            return False

    def is_related(self, other: "Issue") -> bool:
        return self.id_field == other.id_field

    def import_values(
        self,
        data: dict[str, str],
        convert: bool = True,
    ) -> None:
        if not all(key in self._default_attrs for key in data.keys()):
            raise ValueError("data is incomplete")

        for key, value in data.items():
            c_attr = self._attrs_map[key]
            c_attr.set_value(self._source, value)

            if convert:
                setattr(self, key, c_attr.convert(value))
            else:
                setattr(self, key, value)

    def export_values(
        self,
        unconvert: bool = True,
        key_converter: t.Optional[t.Callable[[str], str]] = None,
        exclude_fields: list[str] = None,
    ) -> dict[str, object]:
        data = {}

        for key in self._default_attrs:
            if exclude_fields and key in exclude_fields:
                continue

            key_c = key_converter(key) if key_converter else key

            if unconvert:
                c_attr = self._attrs_map[key]
                data[key_c] = c_attr.unconvert(getattr(self, key))
            else:
                data[key_c] = getattr(self, key)

        return data

    def update(self) -> None:
        pass

    def delete(self) -> None:
        pass


class GitlabIssue(Issue):
    ATTRS_MAP = {
        "issue_id": ConvertableAttr("iid", str, int),
        "issue_name": ConvertableAttr("title"),
        "created_at": ConvertableAttr(
            "created_at",
            datetime.fromisoformat,
            lambda x: x.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        ),
        "updated_at": ConvertableAttr(
            "updated_at",
            datetime.fromisoformat,
            lambda x: x.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        ),
        "description": ConvertableAttr("description"),
        "labels": ConvertableAttr(
            "labels",
            # might be broken if , is used in label name
            lambda x: (
                x
                if isinstance(x, list)
                else ",".join(x)
                if isinstance(x, str)
                else []
            ),
            lambda x: x.split(",") if x is not None else [],
        ),
    }

    def __init__(self, source: _GitlabIssue) -> None:
        super().__init__(source, GitlabIssue.ATTRS_MAP)

    def update(self) -> None:
        data = self.export_values(
            exclude_fields=["issue_id", "created_at", "updated_at"],
        )

        for key, value in data.items():
            c_attr = self._attrs_map[key]
            c_attr.set_value(self._source, value)

        self._source.save()

    def delete(self) -> None:
        self._source.delete()


class JiraIssue(Issue):
    ATTRS_MAP = {
        "issue_id": ConvertableAttr("id"),
        "issue_name": ConvertableAttr("fields.summary"),
        "created_at": ConvertableAttr(
            "fields.created",
            lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%f%z"),
            lambda x: x.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        ),
        "updated_at": ConvertableAttr(
            "fields.updated",
            lambda x: datetime.strptime(x, "%Y-%m-%dT%H:%M:%S.%f%z"),
            lambda x: x.strftime("%Y-%m-%dT%H:%M:%S.%f%z"),
        ),
        "description": ConvertableAttr(
            "fields.description",
            lambda x: "" if x is None else x,
            lambda x: None if not x else x,
        ),
        "labels": ConvertableAttr(
            "fields.labels",
            # might be broken if , is used in label name
            lambda x: (
                x
                if isinstance(x, list)
                else ",".join(x)
                if isinstance(x, str)
                else []
            ),
            lambda x: x.split(",") if x is not None else [],
        ),
    }

    def __init__(self, source: _JiraIssue) -> None:
        super().__init__(source, JiraIssue.ATTRS_MAP)

    def key_converter(key: str) -> str:
        return JiraIssue.ATTRS_MAP[key].attr.replace("fields.", "")

    def update(self) -> None:
        data = self.export_values(
            key_converter=JiraIssue.key_converter,
            exclude_fields=DEFAULT_EXCLUDE_FIELDS,
        )

        self._source.update(fields=data)

    def delete(self) -> None:
        self._source.delete()


@dataclass
class IssuePair:
    src: t.Optional[Issue] = field(default=None)
    dst: t.Optional[Issue] = field(default=None)
