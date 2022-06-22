from typing import Any, Dict, List, Tuple, Optional
from nonebot import get_driver, on_command, on_notice
from nonebot.internal.adapter import Bot as BaseBot
from nonebot.adapters.onebot.v11 import (
    Bot,
    Message,
    MessageEvent,
    GroupMessageEvent,
    GroupRecallNoticeEvent,
)
from nonebot.params import Command, CommandArg, RawCommand

from utils.rauthman import isInService
from .config import Config

withdraw_config = Config.parse_obj(get_driver().config.dict())


__help_plugin_name__ = '信息撤回'
__des__ = 'Bot信息撤回'
__author__ = 'MeetWq'
__level__ = '2'
__cmd__ = '''
bot撤回/withdraw <Bot发的倒数第x条信息>
*回复需要撤回的信息，回复“bot撤回”
'''.strip()
__example__ = '''
hoka 撤回 0
'''.strip()
__note__ = '''
- Bot发的倒数第几条信息里，从0开始
- 0-3代表为撤回倒数三条信息'''
__usage__ = f'''{__des__}
作者：{__author__}
权限等级：{__level__}
用法：{__cmd__}
举例：{__example__}
备注：{__note__}'''


msg_ids: Dict[str, List[int]] = {}
max_size = withdraw_config.withdraw_max_size


def get_key(msg_type: str, id: int):
    return f"{msg_type}_{id}"


async def save_msg_id(
    bot: BaseBot, e: Optional[Exception], api: str, data: Dict[str, Any], result: Any
):
    try:
        if api == "send_msg":
            msg_type = data["message_type"]
            id = data["group_id"] if msg_type == "group" else data["user_id"]
        elif api == "send_private_msg":
            msg_type = "private"
            id = data["user_id"]
        elif api == "send_group_msg":
            msg_type = "group"
            id = data["group_id"]
        else:
            return
        key = get_key(msg_type, id)
        msg_id = int(result["message_id"])

        if key not in msg_ids:
            msg_ids[key] = []
        msg_ids[key].append(msg_id)
        if len(msg_ids) > max_size:
            msg_ids[key].pop(0)
    except:
        pass


Bot.on_called_api(save_msg_id)


withdraw = on_command("withdraw", 
                    aliases={"bot撤回"}, 
                    block=True, 
                    rule=isInService("bot撤回", 2))


@withdraw.handle()
async def _(bot: Bot, event: MessageEvent, msg: Message = CommandArg()):
    if isinstance(event, GroupMessageEvent):
        msg_type = "group"
        id = event.group_id
    else:
        msg_type = "private"
        id = event.user_id
    key = get_key(msg_type, id)

    if event.reply:
        msg_id = event.reply.message_id
        try:
            await bot.delete_msg(message_id=msg_id)
            return
        except:
            await withdraw.finish("撤回失败，可能已超时")

    def extract_num(text: str) -> Tuple[int, int]:
        if not text:
            return 0, 1

        if text.isdigit() and 0 <= int(text) < len(msg_ids[key]):
            return int(text), int(text) + 1

        nums = text.split("-")[:2]
        nums = [n.strip() for n in nums]
        if len(nums) == 2 and nums[0].isdigit() and nums[1].isdigit():
            start_num = int(nums[0])
            end_num = min(int(nums[1]), len(msg_ids[key]))
            if end_num > start_num:
                return start_num, end_num
        return 0, 1

    text = msg.extract_plain_text().strip()
    start_num, end_num = extract_num(text)

    res = ""
    message_ids = [msg_ids[key][-num - 1] for num in range(start_num, end_num)]
    for message_id in message_ids:
        try:
            await bot.delete_msg(message_id=message_id)
            msg_ids[key].remove(message_id)
        except:
            if not res:
                res = "撤回失败，可能已超时"
                if end_num - start_num > 1:
                    res = "部分消息" + res
            continue
    if res:
        await withdraw.finish(res)


async def _group_recall(bot: Bot, event: GroupRecallNoticeEvent) -> bool:
    return str(event.user_id) == str(bot.self_id)


withdraw_notice = on_notice(_group_recall)


@withdraw_notice.handle()
async def _(event: GroupRecallNoticeEvent):
    msg_id = event.message_id
    id = event.group_id
    key = get_key("group", id)
    if key in msg_ids and msg_id in msg_ids[key]:
        msg_ids[key].remove(msg_id)