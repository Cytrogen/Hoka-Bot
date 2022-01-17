import random
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent
from util.data import bookofanswers


__usage__ = '''bookofanswer插件
原作者：【FYWinds】
[答案之书] #问题# -> 让hoka为你决定某件事'''
__help_plugin_name__ = "答案之书"
__priority__ = 7


boa = on_command("答案之书", aliases={"答案书"}, priority=7)
@boa.handle()
async def _(bot: Bot, event: MessageEvent):
    await boa.finish(random.choice(bookofanswers))