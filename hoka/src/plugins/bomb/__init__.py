import random
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent
from util.data import bomb


__usage__ = '''bomb插件会让hoka说抖音小学生句子
（句子包括但不限于炸了长图、抖音名言、黑化文学）
[来点小学生] -> 让hoka变成抖音小学生
'''
__help_plugin_name__ = "皱眉文学"
__priority__ = 7


xxs = on_command("小学生", aliases={'来点小学生', 'xxs', '来点xxs', '小学生', '皱眉文学', '虾仁猪心'}, priority=7)
@xxs.handle()
async def _(bot: Bot, event: MessageEvent):
    await xxs.finish(random.choice(bomb), at_sender=True)