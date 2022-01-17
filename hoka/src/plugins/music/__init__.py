from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot
from nonebot.adapters.cqhttp import Message, GroupMessageEvent
from nonebot.adapters.cqhttp.message import MessageSegment
from .data_source import *


__usage__ = f'''music插件
原作者：【kanomahoro】
[点歌] <歌名> -> 从QQ音乐点歌'''
__help_plugin_name__ = 'QQ音乐点歌'
__priority__ = 5


qqmusic = on_command("点歌", priority=5)
@qqmusic.handle()
async def handle(bot: Bot, event: GroupMessageEvent, state: T_State):
    args = str(event.get_message()).strip()
    msg = ''  
    if args !='':
        id =await data_source.qq_search(args)
        if id != '':
            msg=MessageSegment.music(type_='qq',id_=id)
    Msg = Message(msg)
    await qqmusic.finish(Msg)