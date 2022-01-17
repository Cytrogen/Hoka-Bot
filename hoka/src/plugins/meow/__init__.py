from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event


__usage__ = f'''meow插件
[hoka]* -> hoka会回应你的呼唤~'''
__help_plugin_name__ = '呼唤hoka'
__priority__ = 2


meow = on_command("hoka", priority=2)
@meow.handle()
async def handle_send(bot: Bot, event: Event, state: T_State):
    await meow.finish('喵')