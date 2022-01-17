import os
import re
import time
import random
import asyncio
from pathlib import Path
from datetime import datetime
from nonebot import on_message, on_request, on_notice
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import (PRIVATE_FRIEND, Bot, Message, GroupRequestEvent, GroupDecreaseNoticeEvent, MessageEvent,
                                     FriendRequestEvent, Event, GroupUploadNoticeEvent, GroupIncreaseNoticeEvent)
from nonebot.adapters.cqhttp.exception import ActionFailed
from config.config import OWNER, SUPERUSERS, NICKNAME, Config
from config.path_config import IMAGE_PATH, DATA_PATH
from util.utils import FreqLimiter, scheduler
from util.manager import group_manager, plugins2settings_manager, requests_manager
from util.message_builder import image
from models.friend_user import FriendUser
from models.group_info import GroupInfo
from models.group_member_info import GroupInfoUser
from services.log import logger
try:
    import ujson as json
except ModuleNotFoundError:
    import json


__usage__ = f'''invite插件
原作者：【FYWinds】+【HibiKier】
- 用于处理群事件
- 进群欢迎、退群提醒、hoka自身被邀请事件提醒、群文件上传'''
__help_plugin_name__ = "群事件处理"


Config.add_plugin_config("invite_manager", "message",
    f"强制拉{NICKNAME}，{NICKNAME}飞走走！",
    help_="强制拉群后进群回复的内容")
Config.add_plugin_config("invite_manager", "flag",
    True, help_="被强制拉群后是否直接退出", default_value=True)
Config.add_plugin_config("invite_manager", "welcome_msg_cd",
    5, help_="群欢迎消息cd", default_value=5)
Config.add_plugin_config("_task", "DEFAULT_GROUP_WELCOME",
    True, help_="被动 进群欢迎 进群默认开关状态", default_value=True)
Config.add_plugin_config("_task", "DEFAULT_REFUND_GROUP_REMIND",
    True, help_="被动 退群消息 进群默认开关状态", default_value=True)


_flmt = FreqLimiter(Config.get_config("invite_manager", "welcome_msg_cd"))
exists_data = {"private": {}, "group": {}}


group_increase_handle = on_notice(priority=1, block=False)
@group_increase_handle.handle()
async def _(bot: Bot, event: GroupIncreaseNoticeEvent, state: dict):
    if event.user_id == int(bot.self_id):
        group = await GroupInfo.get_group_info(event.group_id)
        if (not group or group.group_flag == 0) and Config.get_config("invite_manager", "flag"):
            try:
                msg = Config.get_config("invite_manager", "message")
                if msg:
                    await bot.send_group_msg(group_id=event.group_id, message=msg)
                await bot.set_group_leave(group_id=event.group_id)
                await bot.send_private_msg(user_id=int(list(bot.config.superusers)[0]),
                    message=f"触发强制入群保护，已成功退出群聊 {event.group_id}..")
                logger.info(f"强制拉群或未有群信息，退出群聊 {group} 成功")
                requests_manager.remove_request("group", event.group_id)
            except Exception as e:
                logger.info(f"强制拉群或未有群信息，退出群聊 {group} 失败 e:{e}")
                await bot.send_private_msg(user_id=int(list(bot.config.superusers)[0]),
                    message=f"触发强制入群保护，退出群聊 {event.group_id} 失败..")
        elif event.group_id not in group_manager["group_manager"].keys():
            data = plugins2settings_manager.get_data()
            for plugin in data.keys():
                if not data[plugin]["default_status"]:
                    group_manager.block_plugin(plugin, event.group_id)
    else:
        join_time = datetime.now()
        user_info = await bot.get_group_member_info(group_id=event.group_id, user_id=event.user_id)
        if await GroupInfoUser.add_member_info(user_info["user_id"],
            user_info["group_id"],
            user_info["nickname"],
            join_time):
            logger.info(f"用户{user_info['user_id']} 所属{user_info['group_id']} 更新成功")
        else:
            logger.info(f"用户{user_info['user_id']} 所属{user_info['group_id']} 更新失败")

        if await group_manager.check_group_task_status(event.group_id, "group_welcome") and _flmt.check(event.group_id):
            _flmt.start_cd(event.group_id)
            msg = ""
            img = ""
            at_flag = False
            custom_welcome_msg_json = (Path() / "data" / "custom_welcome_msg" / "custom_welcome_msg.json")
            if custom_welcome_msg_json.exists():
                data = json.load(open(custom_welcome_msg_json, "r"))
                if data.get(str(event.group_id)):
                    msg = data[str(event.group_id)]
                    if msg.find("[at]") != -1:
                        msg = msg.replace("[at]", "")
                        at_flag = True
        if os.path.exists(DATA_PATH + f"custom_welcome_msg/{event.group_id}.jpg"):
                img = image(abspath=DATA_PATH + f"custom_welcome_msg/{event.group_id}.jpg")
        if msg or img:
                await group_increase_handle.send("\n" + msg.strip() + img, at_sender=at_flag)
        else:
            await group_increase_handle.send("各位群成员地位-1")


group_decrease_handle = on_notice(priority=1, block=False)
@group_decrease_handle.handle()
async def _(bot: Bot, event: GroupDecreaseNoticeEvent, state: dict):
    if event.sub_type == "kick_me":
        group_id = event.group_id
        operator_id = event.operator_id
        try:
            operator_name = (await GroupInfoUser.get_member_info(event.operator_id, event.group_id)).user_name
        except AttributeError:
            operator_name = "None"
        group = await GroupInfo.get_group_info(group_id)
        group_name = group.group_name if group else ""
        coffee = int(list(bot.config.superusers)[0])
        await bot.send_private_msg(user_id=coffee,
            message=f"hoka被踢报告：\n"
            f"我被 {operator_name}({operator_id})\n"
            f"踢出了 {group_name}({group_id})\n"
            f"日期：{str(datetime.now()).split('.')[0]}")
        return
    if event.user_id == int(bot.self_id):
        group_manager.delete_group(event.group_id)
        return
    try:
        user_name = (await GroupInfoUser.get_member_info(event.user_id, event.group_id)).user_name
    except AttributeError:
        user_name = str(event.user_id)
    if await GroupInfoUser.delete_member_info(event.user_id, event.group_id):
        logger.info(f"用户{user_name}, qq={event.user_id} 所属{event.group_id} 删除成功")
    else:
        logger.info(f"用户{user_name}, qq={event.user_id} 所属{event.group_id} 删除失败")
    if await group_manager.check_group_task_status(event.group_id, "refund_group_remind"):
        rst = ""
        if event.sub_type == "leave":
            rst = f"{user_name}离开了我们……\n这是怎么会是呢？"
        if event.sub_type == "kick":
            operator = await bot.get_group_member_info(user_id=event.operator_id, group_id=event.group_id)
            operator_name = (operator["card"] if operator["card"] else operator["nickname"])
            rst = f"{user_name} 被 {operator_name} 送走了……"
        try:
            await group_decrease_handle.send(f"{rst}")
        except ActionFailed:
            return    


friend_req = on_request(priority=5, block=True)
@friend_req.handle()
async def _(bot: Bot, event: FriendRequestEvent, state: dict):
    global exists_data
    if exists_data["private"].get(event.user_id):
        if time.time() - exists_data["private"][event.user_id] < 60 * 5:
            return
    exists_data["private"][event.user_id] = time.time()
    user = await bot.get_stranger_info(user_id=event.user_id)
    nickname = user["nickname"]
    sex = user["sex"]
    age = str(user["age"])
    comment = event.comment
    await bot.send_private_msg(user_id=int(list(bot.config.superusers)[0]),
        message=f"hoka收到好友请求：\n"
        f"昵称：{nickname}({event.user_id})\n"
        f"自动同意：{'√' if Config.get_config('invite_manager', 'AUTO_ADD_FRIEND') else '×'}\n"
        f"日期：{str(datetime.now()).split('.')[0]}\n"
        f"备注：{event.comment}")
    if Config.get_config("invite_manager", "AUTO_ADD_FRIEND"):
        await bot.set_friend_add_request(flag=event.flag, approve=True)
        await FriendUser.add_friend_info(user["user_id"], user["nickname"])
    else:
        requests_manager.add_request(event.user_id,
            "private",
            event.flag,
            nickname=nickname,
            sex=sex,
            age=age,
            comment=comment)


group_req = on_request(priority=5, block=True)
@group_req.handle()
async def _(bot: Bot, event: GroupRequestEvent, state: dict):
    global exists_data
    if event.sub_type == "invite":
        if str(event.user_id) in bot.config.superusers:
            try:
                if await GroupInfo.get_group_info(event.group_id):
                    await GroupInfo.set_group_flag(event.group_id, 1)
                else:
                    group_info = await bot.get_group_info(group_id=event.group_id)
                    await GroupInfo.add_group_info(group_info["group_id"],
                        group_info["group_name"],
                        group_info["max_member_count"],
                        group_info["member_count"],
                        1)
                await bot.set_group_add_request(flag=event.flag, sub_type="invite", approve=True)
            except ActionFailed:
                pass
        else:
            user = await bot.get_stranger_info(user_id=event.user_id)
            sex = user["sex"]
            age = str(user["age"])
            if exists_data["group"].get(f"{event.user_id}:{event.group_id}"):
                if (time.time()
                    - exists_data["group"][f"{event.user_id}:{event.group_id}"]
                    < 60 * 5):
                    return
            exists_data["group"][f"{event.user_id}:{event.group_id}"] = time.time()
            nickname = await FriendUser.get_user_name(event.user_id)
            await bot.send_private_msg(user_id=int(list(bot.config.superusers)[0]),
                message=f"hoka收到群聊请求：\n"
                f"申请人：{nickname}({event.user_id})\n"
                f"群聊：{event.group_id}\n"
                f"邀请日期：{str(datetime.now()).split('.')[0]}")
            await bot.send_private_msg(user_id=event.user_id,
                message=f"hoka已经提醒{NICKNAME}的管理员大人了\n"
                "请确保已经群主或群管理沟通过！\n"
                "等待管理员处理吧！")
            requests_manager.add_request(event.user_id,
                "group",
                event.flag,
                invite_group=event.group_id,
                nickname=nickname,
                sex=sex,
                age=age)


x = on_message(priority=9, block=False)
@x.handle()
async def _(bot: Bot, event: MessageEvent, state: dict):
    await asyncio.sleep(0.1)
    r = re.search(r'groupcode="(.*?)"', str(event.get_message()))
    if r:
        group_id = int(r.group(1))
    else:
        return
    r = re.search(r'groupname="(.*?)"', str(event.get_message()))
    if r:
        group_name = r.group(1)
    else:
        group_name = "None"
    requests_manager.set_group_name(group_name, group_id)


@scheduler.scheduled_job(
    "interval",
    minutes=5,
)
async def _():
    global exists_data
    exists_data = {"private": {}, "group": {}}


file_upload = on_notice()
@file_upload.handle()
async def fu(bot: Bot, event: GroupUploadNoticeEvent, state: T_State):
    user_name = (await GroupInfoUser.get_member_info(event.user_id, event.group_id)).user_name
    await file_upload.finish(message=Message(f'{user_name} 上传了群文件\n速速来捧场'))