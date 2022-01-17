import shlex
from typing import Type
from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.typing import T_Handler, T_State
from nonebot.adapters.cqhttp import Bot, Event, MessageSegment
from .data_source import create_logo, commands


__usage__ = '''logo插件
原作者：【MeetWq】
[phlogo] <文本1> <文本2>
[tylogo] <文本1> <文本2>
[5000兆] <文本1> <文本2>
[douyin] <文本>
[google] <文本>'''
__help_plugin_name__ = 'logo生成'


async def handle(matcher: Type[Matcher], event: Event, style: str):
    text = event.get_plaintext().strip()
    if not text:
        await matcher.finish()

    arg_num = commands[style]['arg_num']
    texts = [text] if arg_num == 1 else shlex.split(text)
    if len(texts) != arg_num:
        await matcher.finish('参数数量不符')

    image = await create_logo(texts, style)
    if image:
        await matcher.finish(MessageSegment.image(image))
    else:
        await matcher.finish('出错了，请稍后再试')


def create_matchers():

    def create_handler(style: str) -> T_Handler:
        async def handler(bot: Bot, event: Event, state: T_State):
            await handle(matcher, event, style)
        return handler

    for style, params in commands.items():
        matcher = on_command(
            style, aliases=params['aliases'], priority=13)
        matcher.append_handler(create_handler(style))


create_matchers()