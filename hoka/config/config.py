import yaml
from typing import List, Optional, Union
from pathlib import Path
from datetime import timedelta
from ipaddress import IPv4Address
from .utils import ConfigsManager


NICKNAME: str = "hoka"
BOT: str = ""
OWNER: str = ""
SUPERUSERS: List[Union[int, str]] = ["", ""]


# 
MAIN_GROUP: List[Union[int, str]] = ["", ""]
# 
SECOND_GROUP: List[Union[int, str]] = ["", ""]
MAIN_SECOND_GROUP: List[Union[int, str]] = ["", "", ""]
ALL_GROUP: List[Union[int, str]] = ["", "", "", "", ""]


HIDDEN_PLUGINS: List[str] = [
    "nonebot_plugin_apscheduler",
    "nonebot-plugin-flexperm",
    "invite"
]


SUPERUSERS += list(map(int, SUPERUSERS))
SUPERUSERS = list(set(SUPERUSERS))


bind: str = ""
sql_name: str = ""
user: str = ""
password: str = ""
address: str = "127.0.0.1"
port: str = ""
database: str = ""


def load_yml(file: Path, encoding="utf-8") -> dict:
    with open(file, "r", encoding=encoding) as f:
        data = yaml.safe_load(f)
    return data


SYSTEM_PROXY: Optional[str] = "http://127.0.0.1:端口"
Config = ConfigsManager(Path() / "data" / "configs" / "plugins2config.yaml")
