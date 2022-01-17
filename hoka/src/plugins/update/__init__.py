from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from .data_source import *


__usage__ = f'''update插件
[update]* -> 看看hoka的更新小日志吧！
[update history]* -> 看看hoka的小日志历史吧！
'''
__help_plugin_name__ = '更新日志'
__priority__ = 2


update = on_command("update", aliases={'更新', '日志'}, rule=to_me(), priority=2)
@update.handle()
async def handle_send(bot: Bot, event: Event, state: T_State):
    await update.finish(f'''hoka-bot小日志~
1月13日：
- 添加了职业爱豆的训练功能
- 添加了虚假身份生成功能
- 修改了卡池显示
- 新年UP池已关闭，目前UP池为常驻UP池
==========================
- 如果有问题或BUG请使用 [hoka私聊] 来告知我！
--来自hokabot的爹
''')


history = on_command("update history", aliases={'更新历史', '日志历史', 'history'}, rule=to_me(), priority=2)
@history.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["month"] = args

@history.got("month", prompt="你想查询哪月的日志呢？\n日志历史：\n21.10\n21.11\n21.12")
async def handle_city(bot: Bot, event: Event, state: T_State):
    month = state["month"]
    if month in ["10", "十", "10月", "十月", "21.10"]:
        text = october_21()
        await history.finish(text)
    elif month in ["11", "11月", "十一", "十一月", "21.11"]:
        text = november_21()
        await history.finish(text)
    elif month in ["12", "12月", "十二月", "21.12"]:
        text = december_21()
        await history.finish(text)
    elif month in ["1", "1月", "一月", "22.1"]:
        text = january_22()
        await history.finish(text)
        
    month_history = get_month(month)
    await history.finish(month_history)

async def get_month(month: str):
    return f"未查询到该月份的日志！"