import aiohttp
from nonebot import on_regex
from nonebot.adapters.cqhttp import Bot, Event


__usage__ = '''suoxie插件
原作者：【anlen123】
[缩写] <文本> -> 猜测缩写的原文字'''
__help_plugin_name__ = '猜测缩写'


async def get_sx(word):
    url = "https://lab.magiconch.com/api/nbnhhsh/guess"
    headers = {
        'origin': 'https://lab.magiconch.com',
        'referer': 'https://lab.magiconch.com/nbnhhsh/',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36',
    }
    data = {
        "text": f"{word}"
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url, headers=headers, data=data) as resp:
            msg = await resp.json()
            return msg if msg else []


sx = on_regex(pattern="(^sx\ |^缩写\ )")
@sx.handle()
async def sx_rev(bot: Bot, event: Event, state: dict):
    msg = str(event.message).strip()[3:]
    date = await get_sx(msg)
    try:
        name = date[0]['name']
        content = date[0]['trans']
        await bot.send(event=event, message=name + " 可能是：\n" + str(content).replace("[", "").replace("]", "").replace("'", "").replace(",", "，"))
    except :
        await bot.send(event=event, message="没有找到缩写")