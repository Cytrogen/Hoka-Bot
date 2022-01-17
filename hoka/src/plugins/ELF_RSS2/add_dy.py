from nonebot import on_command
from nonebot import permission as su
from nonebot.adapters.cqhttp import Bot, Event, GroupMessageEvent, permission, unescape
from nonebot.rule import to_me
from .RSS import my_trigger as tr
from .RSS import rss_class


RSS_ADD = on_command("add",aliases={"添加订阅", "sub"},rule=to_me(),priority=5,permission=su.SUPERUSER | permission.GROUP_ADMIN | permission.GROUP_OWNER)
@RSS_ADD.handle()
async def handle_first_receive(bot: Bot, event: Event, state: dict):
    args = str(event.get_message()).strip()
    if args:
        state["RSS_ADD"] = unescape(args)

@RSS_ADD.got("RSS_ADD",prompt="请输入\n名称 [订阅地址]\n空格分割、[]表示可选\n私聊默认订阅到当前账号，群聊默认订阅到当前群组\n更多信息可通过 change 命令修改")
async def handle_rss_add(bot: Bot, event: Event, state: dict):
    rss_dy_link = unescape(state["RSS_ADD"])
    user_id = event.get_user_id()
    group_id = None
    if isinstance(event, GroupMessageEvent):
        group_id = event.group_id

    dy = rss_dy_link.split(" ")

    rss = rss_class.Rss()
    try:
        name = dy[0]
    except IndexError:
        await RSS_ADD.send("输入的订阅名为空！")
        return

    async def add_group_or_user(_group_id, _user_id):
        if _group_id:
            rss.add_user_or_group(group=str(_group_id))
            await tr.add_job(rss)
            await RSS_ADD.send("订阅到当前群组成功！")
        else:
            rss.add_user_or_group(user=_user_id)
            await tr.add_job(rss)
            await RSS_ADD.send("订阅到当前账号成功！")

    if rss.find_name(name=name):
        rss = rss.find_name(name=name)
        await add_group_or_user(group_id, user_id)
        return

    try:
        url = dy[1]
    except IndexError:
        await RSS_ADD.send("输入的订阅地址为空！")
        return

    rss.name = name
    rss.url = url
    await add_group_or_user(group_id, user_id)