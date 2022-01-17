import random
from random import randint
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.plugin import on_command
from nonebot.adapters.cqhttp.message import Message
from .data_source import *


__usage__ = f'''tarot插件可以让你抽一张塔罗牌
[抽牌] -> 抽取一张塔罗牌'''
__help_plugin_name__ = "塔罗牌"
__priority__ = 7


tarot = on_command('抽牌', priority=7)
@tarot.handle()
async def tarot_handle(bot: Bot, event: Event, state: T_State):
    rnd = random.Random()
    rnd.seed()
    cardnum = rnd.randint(0,43)
    await tarot.finish(message=Message(f'\n{card(cardnum)}'), at_sender=True)