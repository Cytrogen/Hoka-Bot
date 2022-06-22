import shlex
import traceback
from nonebot import on_command
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.typing import T_Handler
from nonebot.params import CommandArg
from nonebot.plugin import PluginMetadata
from nonebot.adapters.onebot.v11 import MessageSegment, Message

from .data_source import commands, Command

from utils.rauthman import isInService


__help_plugin_name__ = 'Logo制作'
__des__ = 'Logo制作'
__author__ = 'MeetWq'
__level__ = '1'
__cmd__ = '''
hoka ph/phlogo <左> <右>
hoka yt/ytlogo <左> <右>
hoka 5000兆 <左> <右>
hoka douyin/dylogo <文字>
hoka google/gglogo <文字>
'''.strip()
__example__ = '''
hoka 5000兆 我去 初音未来！
'''.strip()
__note__ = '''
- N/A'''
__usage__ = f'''{__des__}
作者：{__author__}
权限等级：{__level__}
用法：{__cmd__}
举例：{__example__}
备注：{__note__}'''


def create_matchers():
    def create_handler(command: Command) -> T_Handler:
        async def handler(matcher: Matcher, msg: Message = CommandArg()):
            text = msg.extract_plain_text().strip()
            if not text:
                await matcher.finish()

            arg_num = command.arg_num
            if arg_num == 1:
                texts = [text]
            else:
                try:
                    texts = shlex.split(text)
                except:
                    texts = text.split()
            if len(texts) != arg_num:
                await matcher.finish(f"参数数量不符，需要发送{arg_num}段文字")

            try:
                image = await command.func(texts)
            except:
                logger.warning(traceback.format_exc())
                await matcher.finish("出错了，请稍后再试")

            await matcher.finish(MessageSegment.image(image))

        return handler

    for command in commands:
        on_command(command.keywords[0], 
                aliases=set(command.keywords), 
                priority=13, 
                rule=isInService("logo制作", 1),
                block=True).append_handler(create_handler(command))


create_matchers()