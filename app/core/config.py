from pydantic_settings import BaseSettings


class Config(BaseSettings):
    service_name: str = "service_name"
    # TODO: wtf is this, remove
    secret_key: str = "s3cr3t_k3y"


config = Config()
