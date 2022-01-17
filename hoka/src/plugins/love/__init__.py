import random
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, MessageEvent
from util.data import twqh


__usage__ = f'''love插件会让hoka说土味情话
[我爱你]* -> 让hoka向你表白
'''
__help_plugin_name__ = '土味情话'
__priority__ = 7


love = on_command("我爱你", aliases={'爱你', '爱死你'}, rule=to_me(), priority=7)
@love.handle()
async def _(bot: Bot, event: MessageEvent):
    await love.finish(random.choice(twqh), at_sender=True)