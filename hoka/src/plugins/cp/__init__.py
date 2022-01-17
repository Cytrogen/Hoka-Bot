import random
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, Event
from util.data import cp


__usage__ = '''cp插件
原作者：【AkashiCoin】
[cp] <攻> <受>
[cp] [@] [@]'''
__help_plugin_name__ = 'CP文生成'


CPg = on_command("cp", priority=7)
@CPg.handle()
async def _(bot: Bot, event: Event, state: T_State):
    msg = event.get_message()
    msg_text = event.get_plaintext().strip()
    name_list = [f"{event.user_id}"]
    for msg_seg in msg:
        if msg_seg.type == "at":
            name_list.append(msg_seg.data["qq"])
    num = len(name_list)
    if num > 1:
        if num > 2:
            del name_list[0]
        for i in range(len(name_list)):
            user_name = await bot.get_group_member_info(group_id=event.group_id, user_id=name_list[i])
            user_name = (user_name["card"] if user_name["card"] else user_name["nickname"])
            name_list = user_name
    else:
        del name_list[0]
        msg_text = msg_text.split()
        for name in msg_text:
            name_list.append(name)
    await CPg.finish("\n" + getMessage(name_list), at_sender=True)


def getMessage(name_list):
    content = cp
    content = (random.choice(content["data"])
        .replace("<攻>", name_list[0])
        .replace("<受>", name_list[1]))
    return content