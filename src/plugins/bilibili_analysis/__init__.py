import re

from nonebot import on_regex
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageEvent
from nonebot.log import logger

from .analysis_bilibili import b23_extract, bili_keyword
from utils.rauthman import isInService


__help_plugin_name__ = 'B站视频解析'
__des__ = 'Bilibili视频、番剧解析'
__author__ = 'mengshouer + NekoAria'
__level__ = '1'
__cmd__ = '''
发送Bilibili视频链接、小程序、BV号等
'''.strip()
__example__ = '''
BV114514
'''.strip()
__note__ = '''
- N/A'''
__usage__ = f'''{__des__}
作者：{__author__}
权限等级：{__level__}
用法：{__cmd__}
举例：{__example__}
备注：{__note__}'''


analysis_bili = on_regex(
    r"(b23.tv)|(bili(22|23|33|2233).cn)|(.bilibili.com)|(^(av|cv)(\d+))|(^BV([a-zA-Z0-9]{10})+)|"
    r"(\[\[QQ小程序\]哔哩哔哩\])|(QQ小程序&amp;#93;哔哩哔哩)|(QQ小程序&#93;哔哩哔哩)",
    flags=re.I,
    rule=isInService("B站视频解析", 1))


@analysis_bili.handle()
async def analysis_main(event: MessageEvent) -> None:
    text = str(event.message).strip()
    if re.search(r"(b23.tv)|(bili(22|23|33|2233).cn)", text, re.I):
        # 提前处理短链接，避免解析到其他的
        text = await b23_extract(text)
    group_id = event.group_id if isinstance(event, GroupMessageEvent) else None
    msg = await bili_keyword(group_id, text)
    if msg:
        try:
            await analysis_bili.send(msg)
        except Exception as e:
            logger.error(e)