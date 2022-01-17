from pydantic import Field, BaseSettings


class Config(BaseSettings):
    apscheduler_autostart: bool = True
    apscheduler_log_level: int = 30
    apscheduler_config: dict = Field(default_factory=lambda: ("America/New_York"))

    class Config:
        extra = "ignore"