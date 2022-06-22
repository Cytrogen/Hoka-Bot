from io import BytesIO
from typing import Union
from nonebot.params import Depends
from nonebot.matcher import Matcher
from nonebot.typing import T_Handler
from nonebot.plugin import PluginMetadata
from nonebot import on_command, on_message, require
from nonebot.adapters.onebot.v11 import MessageSegment

require("nonebot_plugin_imageutils")

from .depends import regex
from .data_source import memes
from .utils import Meme, help_image, isInService


__help_plugin_name__ = '表情包制作'
__des__ = '表情包制作'
__author__ = 'MeetWq'
__level__ = '1'
__cmd__ = '''
表情包制作
hoka <表情包名> <文字>
'''.strip()
__example__ = '''
hoka 鲁迅说 我没说过这句话
'''.strip()
__note__ = '''
- N/A'''
__usage__ = f'''{__des__}
作者：{__author__}
权限等级：{__level__}
用法：{__cmd__}
举例：{__example__}
备注：{__note__}'''


help_cmd = on_command("表情包制作", 
                    block=True,
                    priority=12,
                    rule=isInService("表情包制作", 1))


@help_cmd.handle()
async def _():
    img = await help_image(memes)
    if img:
        await help_cmd.finish(MessageSegment.image(img))


def create_matchers():
    def handler(meme: Meme) -> T_Handler:
        async def handle(
            matcher: Matcher, res: Union[str, BytesIO] = Depends(meme.func)
        ):
            matcher.stop_propagation()
            if isinstance(res, str):
                await matcher.finish(res)
            await matcher.finish(MessageSegment.image(res))

        return handle

    for meme in memes:
        on_message(
            regex(meme.pattern),
            block=False,
            priority=12
        ).append_handler(handler(meme))


create_matchers()
