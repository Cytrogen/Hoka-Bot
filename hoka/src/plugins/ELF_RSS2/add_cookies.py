from nonebot import on_command
from nonebot import permission as su
from nonebot.rule import to_me
from nonebot.adapters.cqhttp import Bot, Event, permission, unescape
from .RSS import my_trigger as tr
from .RSS import rss_class


ADD_COOKIES = on_command("add_cookies",aliases={"添加cookies"},rule=to_me(),priority=5,permission=su.SUPERUSER | permission.GROUP_ADMIN | permission.GROUP_OWNER,)
@ADD_COOKIES.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    args = str(event.get_message()).strip()
    if args:
        state["ADD_COOKIES"] = unescape(args)


prompt = (
    "请输入：\n"
    "名称 cookies\n"
    "空格分割\n"
    "获取方式：\n"
    "PC端 chrome 浏览器按 F12\n"
    "找到Console选项卡，输入:\n"
    "document.cookie\n"
    "输出的字符串就是了"
)


@ADD_COOKIES.got("ADD_COOKIES", prompt=prompt)
async def handle_add_cookies(bot: Bot, event: Event, state: dict):
    rss_cookies = unescape(state["ADD_COOKIES"])

    dy = rss_cookies.split(" ", 1)

    rss = rss_class.Rss()
    try:
        name = dy[0]
    except IndexError:
        await ADD_COOKIES.send("输入的订阅名为空！")
        return

    if not rss.find_name(name=name):
        await ADD_COOKIES.send(f"不存在该订阅: {name}")
        return
    rss = rss.find_name(name=name)

    try:
        cookies = dy[1]
    except IndexError:
        await ADD_COOKIES.send("输入的cookies为空！")
        return

    rss.name = name
    if rss.set_cookies(cookies):
        await tr.add_job(rss)
        await ADD_COOKIES.send(f"{rss.name}的Cookies添加成功！\nCookies:{rss.cookies}\n")
    else:
        await ADD_COOKIES.send(f"{rss.name}的Cookies添加失败！\nCookies:{rss.cookies}\n")
