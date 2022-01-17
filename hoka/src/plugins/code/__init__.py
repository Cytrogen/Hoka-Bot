from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, Event, Message
from .run import run


__usage__ = """code插件
原作者：【yzyyz1387】
[code] <语言> #-i# #输入#
    [代码]

【-i：输入，后跟输入内容】
【目前仅支持 c/cpp/c#/py/php/go/java/js 】
"""
__help_plugin_name__ = "在线运行代码"
__priority__ = 8


runcode = on_command('code', priority=8)
@runcode.handle()
async def _(bot: Bot, event: Event):
    code = str(event.get_message()).strip()
    res = await run(code)
    await runcode.send(message=Message(res))