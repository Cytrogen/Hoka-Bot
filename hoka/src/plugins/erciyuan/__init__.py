import random
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent
from util.data import erciyuan


__usage__ = '''erciyuan插件会让hoka说二次元句子
（句子包含但不限于动漫梗、中二病、B站用户名言）
[来点二次元] -> 让hoka变成二次元
'''
__help_plugin_name__ = "二次元句子"
__priority__ = 7


ecy = on_command("来点二次元", aliases={'二次元', '来点二刺螈', '二刺螈'}, priority=7)
@ecy.handle()
async def _(bot: Bot, event: MessageEvent):
    await ecy.finish(random.choice(erciyuan), at_sender=True)