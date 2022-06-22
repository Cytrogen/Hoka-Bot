import aiohttp
from nonebot.plugin import on_regex
from nonebot.params import T_State, State
from nonebot.adapters.onebot.v11 import Bot, Event
from numpy import isin

from utils.rauthman import isInService


__help_plugin_name__ = '缩写猜测'
__des__ = '缩写查询器'
__author__ = 'anlen123'
__level__ = '1'
__cmd__ = '''
[缩写] <缩写>
'''.strip()
__example__ = '''
缩写 nbcs
'''.strip()
__note__ = '''
- N/A'''
__usage__ = f'''{__des__}
作者：{__author__}
权限等级：{__level__}
用法：{__cmd__}
举例：{__example__}
备注：{__note__}'''


async def get_sx(word):
    url = "https://lab.magiconch.com/api/nbnhhsh/guess"
    headers = {
        'origin': 'https://lab.magiconch.com',
        'referer': 'https://lab.magiconch.com/nbnhhsh/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'}
    data = {"text": f"{word}"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, headers=headers, data=data) as resp:
            msg = await resp.json()
            return msg if msg else []


sx = on_regex(pattern="^sx\ |^缩写\ (.*)",
            rule=isInService("缩写猜测", 1))
@sx.handle()
async def _(bot: Bot, event: Event, state: T_State = State()):
    msg = str(event.get_message())[3:]
    data = await get_sx(msg)
    try:
        name = data[0]['name']
        content = data[0]['trans']
        await bot.send(event=event, message=name + " 可能是：\n" + str(content).replace("[", "").replace("]", "").replace("'", "").replace(",", "，"))
    except :
        await bot.send(event=event, message="没有找到缩写")