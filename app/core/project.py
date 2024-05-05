from dataclasses import dataclass


@dataclass
class Project:
    tracker: str
    project_id: str
    name: str
