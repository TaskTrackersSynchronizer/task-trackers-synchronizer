from pydantic_settings import BaseSettings
from typing import List


class Config(BaseSettings):
    service_name: str = "task_trackers_synchronizer"
    # TODO: override
    secret_key: str = "s3cr3t_k3y"
    task_trackers: List[str] = ["Jira", "Gitlab"]


config = Config()
