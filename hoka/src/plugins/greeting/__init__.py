import random
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event


__usage__ = '''greeting插件是让你和hoka打招呼的好东西
[早上/中午/下午/晚上好] -> 打招呼是好习惯喔！
'''
__help_plugin_name__ = '打招呼'
__priority__ = 10


morning = on_command("早上好", aliases={'早安'}, priority=10)
@morning.handle()
async def _(bot: Bot, event: Event, state: T_State):
    await morning.finish(random.choice(['又是新的一天呢！', 
    '早上好呀！',
    '早安呢',
    '早安喵']))


noon = on_command("中午好", aliases={'午安'}, priority=10)
@noon.handle()
async def _(bot: Bot, event: Event, state: T_State):
    await noon.finish(random.choice(['中午好呀！',
    '中午吃什么呢',
    '午安喵']))


afternoon = on_command("下午好", priority=10)
@afternoon.handle()
async def _(bot: Bot, event: Event, state: T_State):
    await afternoon.finish(random.choice(['下午好呢',
    '下午了，吃饭没']))


night = on_command("晚上好", priority=10)
@night.handle()
async def _(bot: Bot, event: Event, state: T_State):
    await night.finish(random.choice(['晚上好呀',
    '要去睡觉了呢']))


sleep = on_command("晚安", priority=10)
@sleep.handle()
async def _(bot: Bot, event: Event, state: T_State):
    await sleep.finish(random.choice(['晚安啦',
    '快睡吧',
    '不要熬夜哦']))