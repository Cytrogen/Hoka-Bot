from faker import Faker
from nonebot import on_regex
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event


__usage__ = '''fakeinfo插件
[虚假身份] #男/女# #生日# -> 指定男/女生成姓名，指定生日生成随机日期'''
__help_plugin_name__ = '随机身份'
f = Faker(locale='zh_CN')


fakeinfo = on_regex("虚假身份(男|女)?(生日)?", priority=10)
@fakeinfo.handle()
async def _(bot: Bot, event: Event, state: T_State):
    info = state["_matched_groups"]
    info = list(info)

    if info[0]:
        info[0] = str(info[0])
    if '男' in info[0]:
        name = f.name_male() + '\n男'
    elif '女' in info[0]:
        name = f.name_female() + '\n女'

    if info[1]:
        date = f.date()
        date = date[5:]
    else:
        await fakeinfo.finish(name)
    await fakeinfo.finish(name + '\n' + date)