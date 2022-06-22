import requests
from .config import Config
from nonebot import require
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import json
import nonebot
from nonebot.adapters.onebot.v11 import Message


__help_plugin_name__ = '60秒读世界'
__des__ = '60秒读世界'
__author__ = 'binggganhe123'
__level__ = '需要联系Bot管理员手动开启'
__cmd__ = '''
N/A
'''.strip()
__example__ = '''
N/A
'''.strip()
__note__ = '''
- N/A'''
__usage__ = f'''{__des__}
作者：{__author__}
权限等级：{__level__}
用法：{__cmd__}
举例：{__example__}
备注：{__note__}'''


global_config = nonebot.get_driver().config
nonebot.logger.info("global_config:{}".format(global_config))
plugin_config = Config(**global_config.dict())
nonebot.logger.info("plugin_config:{}".format(plugin_config))
scheduler = require("nonebot_plugin_apscheduler").scheduler  # type:AsyncIOScheduler


def remove_upprintable_chars(s):
    return ''.join(x for x in s if x.isprintable())#去除imageUrl可能存在的不可见字符


async def read60s():
    #global msg  # msg改成全局，方便在另一个函数中使用
    msg = await suijitu()
    for qq in plugin_config.read_qq_friends:
        await nonebot.get_bot().send_private_msg(user_id=qq, message=Message(msg))

    for qq_group in plugin_config.read_qq_groups:
        await nonebot.get_bot().send_group_msg(group_id=qq_group, message=Message(msg))# MessageEvent可以使用CQ发图片


async def suijitu():
    try:
        url="https://api.iyk0.com/60s"
        resp = requests.get(url)
        resp = resp.text
        resp = remove_upprintable_chars(resp)
        retdata = json.loads(resp)
        lst = retdata['imageUrl']
        pic_ti = f"今日60S读世界已送达\n[CQ:image,file={lst}]"
        return pic_ti
    except:
        url = "https://api.2xb.cn/zaob"#备用网址
        resp = requests.get(url)
        resp = resp.text
        resp = remove_upprintable_chars(resp)
        retdata = json.loads(resp)
        lst = retdata['imageUrl']
        pic_ti1 = f"今日60S读世界已送达\n[CQ:image,file={lst}]"
        return pic_ti1

for index, time in enumerate(plugin_config.read_inform_time):
    nonebot.logger.info("id:{},time:{}".format(index, time))
    scheduler.add_job(read60s, "cron", hour=time.hour, minute=time.minute, id=str(index))