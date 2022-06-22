import asyncio

import arrow
import nonebot
from nonebot import on_metaevent, require
from nonebot.adapters.onebot.v11 import Event, LifecycleMetaEvent
from nonebot.log import logger

from . import command
from . import my_trigger as tr
from .config import DATA_PATH, config
from .rss_class import Rss

from utils.rauthman import isInService


__help_plugin_name__ = 'RSS订阅'
__des__ = 'RSS订阅'
__author__ = 'Quan666'
__level__ = '3 & 群管理员+'
__cmd__ = '''
add/添加订阅/sub <订阅名> <RSS地址>
rsshub_add <RSSHub路由名> <订阅名>
deldy/删除订阅/drop <订阅名>
show_all/showall/select_all/selectall/所有订阅 <关键词>
show/查看订阅 <订阅名>
change/修改订阅/moddy <订阅名> <属性>=<值>
'''.strip()
__example__ = '''
add 鸽了几年投稿的我 bilibili/user/video/337646870
deldy 鸽了几年投稿的我
showall 鸽了
change 鸽了几年投稿的我 stop=1
'''.strip()
__note__ = '''
- RSS地址见[https://docs.rsshub.app/]
- 关键词支持正则，过滤生效范围为订阅名、订阅地址、QQ号、群号
- 修改订阅的属性表见[https://github.com/Quan666/ELF_RSS/blob/2.0/docs/2.0%20%E4%BD%BF%E7%94%A8%E6%95%99%E7%A8%8B.md#%E4%BF%AE%E6%94%B9%E8%AE%A2%E9%98%85]'''
__usage__ = f'''{__des__}
作者：{__author__}
权限等级：{__level__}
用法：{__cmd__}
举例：{__example__}
备注：{__note__}'''


scheduler = require("nonebot_plugin_apscheduler").scheduler
START_TIME = arrow.now()


async def check_first_connect(event: Event) -> bool:
    return isinstance(event, LifecycleMetaEvent) and arrow.now() < START_TIME.shift(
        minutes=1
    )


start_metaevent = on_metaevent(rule=check_first_connect,
                                block=True)


# 启动时发送启动成功信息
@start_metaevent.handle()
async def start() -> None:
    bot = nonebot.get_bot()

    # 启动后检查 data 目录，不存在就创建
    if not DATA_PATH.is_dir():
        DATA_PATH.mkdir()

    boot_message = (
        f"Version: {config.version}\n"
        "Author：Quan666\n"
        "https://github.com/Quan666/ELF_RSS"
    )

    rss_list = Rss.read_rss()  # 读取list
    if not rss_list:
        logger.info("第一次启动，你还没有订阅，记得添加哟！")
    logger.info("ELF_RSS 订阅器启动成功！")
    # 创建检查更新任务
    await asyncio.gather(*[tr.add_job(rss) for rss in rss_list if not rss.stop])
