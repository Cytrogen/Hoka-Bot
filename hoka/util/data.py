import json
from nonebot.log import logger
from config.path_config import TEXT_PATH

bookofanswers: list[str]
erciyuan: list[str]
bomb: list[str]
twqh: list[str]
cp: list[str]

with open(f"{TEXT_PATH}bookofanswers.json", "r", encoding="utf-8") as file:
    bookofanswers = json.load(file)

with open(f"{TEXT_PATH}erciyuan.json", "r", encoding="utf-8") as file:
    erciyuan = json.load(file)

with open(f"{TEXT_PATH}bomb.json", "r", encoding="utf-8") as file:
    bomb = json.load(file)

with open(f"{TEXT_PATH}gedeng.json", "r", encoding="utf-8") as file:
    gedeng = json.load(file)

with open(f"{TEXT_PATH}twqh.json", "r", encoding="utf-8") as file:
    twqh = json.load(file)

with open(f"{TEXT_PATH}cp.json", "r", encoding="utf-8") as file:
    cp = json.load(file)