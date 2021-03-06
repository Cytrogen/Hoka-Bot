import re

import httpx
from nonebot import on_startswith
from nonebot.adapters.onebot.v11 import GroupMessageEvent, MessageSegment
from nonebot.matcher import Matcher

from utils.rauthman import isInService


__help_plugin_name__ = 'B站视频封面提取'
__des__ = 'Bilibili视频封面提取'
__author__ = 'A-kirami'
__level__ = '1'
__cmd__ = '''
提取封面 <视频链接/AV号/BV号>
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


bilibili_cover_matcher = on_startswith(("提取封面","B站封面","bilibili封面","B站封面提取"),
                                        rule=isInService("B站视频封面提取", 1))

@bilibili_cover_matcher.handle()
async def bilibili_cover(event: GroupMessageEvent, matcher: Matcher):
    msg = event.message.extract_plain_text()
    params = {}
    if vc_match := re.search(r"(?P<bv>bv\w+)|(?P<av>av\d+)", msg, re.I):
        if bvid := vc_match["bv"]:
            params["bvid"] = bvid
        elif aid := vc_match["av"]:
            params["aid"] = aid
    else:
        await matcher.finish("请输入BV号或AV号或视频地址")
    url = "https://api.bilibili.com/x/web-interface/view"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36",
        "Referer": "https://www.bilibili.com",
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
    if response.is_success:
        content = response.json()
        cover_url = content.get("data").get("pic")
        await matcher.finish(MessageSegment.image(cover_url))
    else:
        await matcher.finish("该视频不存在")