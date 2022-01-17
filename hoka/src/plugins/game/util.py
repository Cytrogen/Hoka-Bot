import os
import time
import locale
import nonebot
from typing import List
from pathlib import Path
from pydantic import BaseModel, Field
from nonebot.adapters.cqhttp import GroupMessageEvent
try:
    import ujson as json
except ModuleNotFoundError:
    import json


driver: nonebot.Driver = nonebot.get_driver()
game_path = driver.config.game_path if driver.config.game_path else ''


player_data = {}
if game_path:
    file = Path(game_path) / 'game_data.json'
    file.parent.mkdir(exist_ok=True, parents=True)
    if file.exists():
        player_data = json.load(open(file, 'r', encoding='utf8'))
    else:
        old_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'game_data.json'))
        if os.path.exists(old_file):
            os.rename(old_file, file)
            player_data = json.load(open(file, 'r', encoding='utf8'))
else:
    file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'game_data.json'))
    if os.path.exists(file):
        player_data = json.load(open(file, 'r', encoding='utf8'))


def get_message_text(data: str) -> str:
    data = json.loads(data)
    result = ''
    try:
        for msg in data['message']:
            if msg['type'] == 'text':
                result += msg['data']['text'].strip() + ' '
        return result.strip()
    except Exception:
        return ''


def get_message_at(data: str) -> list:
    qq_list = []
    data = json.loads(data)
    try:
        for msg in data['message']:
            if msg['type'] == 'at':
                qq_list.append(int(msg['data']['qq']))
        return qq_list
    except Exception:
        return []


def is_number(s) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


def luck_simple(num):
    if num < 18:
        return '凶'
    elif num < 53:
        return '末吉'
    elif num < 58:
        return '末小吉'
    elif num < 62:
        return '小吉'
    elif num < 71:
        return '半吉'
    elif num < 83:
        return '吉'
    else:
        return '大吉'


def job_finder(event: GroupMessageEvent):
    job = player_data[str(event.group_id)][str(event.user_id)]['job']
    if job == 0:
        msg = '无业'
    elif job == 1:
        msg = '爱豆'
    elif job == 2:
        msg = '传教士'
    return msg


def dates():
    locale.setlocale(locale.LC_CTYPE, 'chinese')
    return time.strftime('\n%y年%#m月%#d日 %#I:%#M\n')


def player_is_exists(event: GroupMessageEvent) -> dict:
    global player_data
    user_id = str(event.user_id)
    group_id = str(event.group_id)
    nickname = event.sender.card if event.sender.card else event.sender.nickname
    if group_id not in player_data.keys():
        player_data[group_id] = {}
    if user_id not in player_data[group_id].keys():
        player_data[group_id][user_id] = {
            'user_id': user_id,
            'group_id': group_id,
            'nickname': nickname,
            'gold': 0,
            'make_gold': 0,
            'lose_gold': 0,
            'win_count': 0,
            'lose_count': 0,
            'is_sign': False,
            'is_work': False,
            'is_job': False,
            'is_belief': False,
            'is_jail': False,
            'is_teach': False,
            'is_study': 0,
            'is_train': False,
            'job': 0,
            'sing': 0,
            'popular': 0,
            'happy': 0,
            'jail': 0,
            'wisdom': 0,
            'num6': 0,
            'num5': 0,
            'num4': 0,
            'num3': 0,
            'num1': 0
        }
    return player_data