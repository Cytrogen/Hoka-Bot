import os
from pathlib import Path
from typing import Any, List
from nonebot import get_driver, logger
from nonebot.config import BaseConfig
from pydantic import AnyHttpUrl, Extra


DATA_PATH = Path.cwd() / "data"
JSON_PATH = DATA_PATH / "rss.json"


class ELFConfig(BaseConfig):
    class Config:
        extra = Extra.allow

    rss_proxy: str = ""
    rsshub: AnyHttpUrl = "https://rsshub.app"
    rsshub_backup: List[AnyHttpUrl] = []
    db_cache_expire = 30
    limit = 50

    zip_size: int = 2 * 1024

    gif_zip_size: int = 6 * 1024

    blockquote: bool = True
    black_word: List[str] = []

    baidu_id: str = ""
    baidu_key: str = ""

    is_linux: bool = os.name != "nt"

    is_open_auto_down_torrent: bool = False
    qb_web_url: str = "http://127.0.0.1:8081"
    qb_down_path: str = ""
    down_status_msg_group: List[int] = []
    down_status_msg_date: int = 10

    max_length: int = 0

    version: str = ""

    def __getattr__(self, name: str) -> Any:
        data = self.dict()
        for k, v in data.items():
            if k.casefold() == name.casefold():
                return v
        return None

config = ELFConfig(**get_driver().config.dict())
logger.debug(f"RSS Config loaded: {config!r}")