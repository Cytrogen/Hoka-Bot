# python3
# -*- coding: utf-8 -*-
# @Time    : 2021/12/23 0:52
# @Author  : yzyyz
# @Email   :  youzyyz1384@qq.com
# @File    : __init__.py.py
# @Software: PyCharm

import json
from asyncio import sleep as asleep
from traceback import print_exc
from random import randint

import nonebot
from nonebot import on_command, logger, on_notice
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, NoticeEvent
from nonebot.adapters.onebot.v11 import ActionFailed
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.permission import SUPERUSER
from . import approve, group_request_verify, group_request, notice, utils, word_analyze, auto_ban, switcher
from .utils import At, Reply, MsgText, banSb, init, check_func_status
from .group_request_verify import verify
from .config import plugin_config, global_config


__help_plugin_name__ = '简易群管'
__des__ = '简易群管'
__author__ = 'yzyyz1387'
__level__ = '该插件拥有独立的权限系统'
__cmd__ = '''

群管初始化

【禁言】
禁 <@> <秒/不写则随机/0为解禁>
解 <@>

【全群禁言】
/all

【群名片/群头衔】
改 <@> <群名片>
头衔 <@> <头衔>
删头衔

【踢/拉黑】
踢 <@>
黑 <@>

【撤回】
（回复要撤回的信息）撤回
撤回 <@> <历史信息倍数5>

【管理员】
管理员+ <@>
管理员- <@>

【加群自动审批】
查看词条
词条+ <词条>
词条- <词条>

【超级用户独占】
所有词条
指定词条+ <群号> <词条>
指定词条- <群号> <词条>
查看分管
所有分管
群管接收

【分群管理员设置】
分管+ <@>
分管- <@>

【群词云统计】
记录本群
停止记录本群
群词云

【违禁词检测】
简单违禁词
严格违禁词
更新违禁词库

【功能开关】
开关 <功能名>
开关状态

'''.strip()
__example__ = '''
禁 @9191810 114514
改 @9191810 暖男我修院
开关 违禁词

'''.strip()
__note__ = '''
- 分群管理员/分管为可以接受加群处理结果信息的用户
- 功能开关的功能名：
    -- 管理、踢、禁、改、基础群管
    -- 加群、审批、加群审批、自动审批
    -- 词云、群词云、wordcloud
    -- 违禁词、违禁词检测
- 功能开关的所有功能默认开启
'''
__usage__ = f'''{__des__}
作者：{__author__}
权限等级：{__level__}
用法：{__cmd__}
举例：{__example__}
备注：{__note__}'''


su = global_config.superusers
cb_notice = plugin_config.callback_notice


admin_init = on_command('群管初始化', priority=1, block=True, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)
@admin_init.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    await init()


ban = on_command('禁', priority=1, block=True, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)
@ban.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    """
    /禁 @user 禁言
    """
    # msg = str(event.get_message()).replace(" ", "").split("]")
    msg = MsgText(event.json())
    sb = At(event.json())
    gid = event.group_id
    status = await check_func_status("admin", str(gid))
    if status:
        if sb:
            if len(msg.split(" ")) > 1:
                try:
                    time = int(msg.split(" ")[-1])
                except ValueError:
                    time = None  # 出现错误就默认随机 【理论上除非是 /撤回 @user n 且 n 不是数值时才有可能触发】
            else:
                time = None
            baning = banSb(gid, ban_list=sb, time=time)
            try:
                async for baned in baning:
                    if baned:
                        await baned
            except ActionFailed:
                await ban.finish("权限不足")
            else:
                logger.info("禁言操作成功")
                if cb_notice:  # 迭代结束再通知
                    if time is not None:
                        await ban.finish("禁言操作成功")
                    else:
                        await ban.finish("该用户已被禁言随机时长")
        else:
            pass
    else:
        await ban.send(f"功能处于关闭状态，发送【开关管理】开启")


unban = on_command("解", priority=1, block=True, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)


@unban.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    """
    /解 @user 解禁
    """
    sb = At(event.json())
    gid = event.group_id
    status = await check_func_status("admin", str(gid))
    if status:
        if sb:
            baning = banSb(gid, ban_list=sb, time=0)
            try:
                async for baned in baning:
                    if baned:
                        await baned
            except ActionFailed:
                await unban.finish("权限不足")
            else:
                logger.info("解禁操作成功")
                if cb_notice:  # 迭代结束再通知
                    await unban.finish("解禁操作成功")
    else:
        await unban.send(f"功能处于关闭状态，发送【开关管理】开启")


ban_all = on_command("/all", aliases={"全员"}, permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER, priority=1, block=True)


@ban_all.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    """
    （测试时没用..） 
    # note: 如果在 .env.* 文件内设置了 COMMAND_START ，且不包含 "" (即所有指令都有前缀，假设 '/' 是其中一个前缀)，则应该发 //all 触发 
    /all 全员禁言
    /all  解 关闭全员禁言
    """
    msg = event.get_message()
    if msg and '解' in str(msg):
        enable = False
    else:
        enable = True
    try:
        await bot.set_group_whole_ban(
            group_id=event.group_id,
            enable=enable
        )
    except ActionFailed:
        await ban_all.finish("权限不足")
    else:
        logger.info(f"全体操作成功: {'禁言' if enable else '解禁'}")
        if cb_notice:
            await ban_all.finish(f"全体操作成功: {'禁言' if enable else '解禁'}")


change = on_command('改', permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER, priority=1, block=True)


@change.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    """
    /改 @user xxx 改群昵称
    """
    msg = str(event.get_message())
    logger.info(msg.split())
    sb = At(event.json())
    gid = event.group_id
    status = await check_func_status("admin", str(gid))
    if status:
        if sb:
            try:
                for user_ in sb:
                    await bot.set_group_card(
                        group_id=gid,
                        user_id=int(user_),
                        card=msg.split()[-1:][0]
                    )
            except ActionFailed:
                await change.finish("权限不足")
            else:
                logger.info("改名片操作成功")
                if cb_notice:
                    await change.finish("改名片操作成功")
    else:
        await change.send(f"功能处于关闭状态，发送【开关管理】开启")


title = on_command('头衔', permission=SUPERUSER | GROUP_OWNER, priority=1, block=True)


@title.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    """
    /头衔 @user  xxx  给某人头衔
    """
    msg = str(event.get_message())
    stitle = msg.split()[-1:][0]
    logger.info(str(msg.split()), stitle)
    sb = At(event.json())
    gid = event.group_id
    status = await check_func_status("admin", str(gid))
    if status:
        if sb:
            if 'all' not in sb:
                try:
                    for qq in sb:
                        await bot.set_group_special_title(
                            group_id=gid,
                            user_id=int(qq),
                            special_title=stitle,
                            duration=-1,
                        )
                except ActionFailed:
                    await title.finish("权限不足")
                else:
                    logger.info(f"改头衔操作成功{stitle}")
                    if cb_notice:
                        await title.finish(f"改头衔操作成功{stitle}")
            else:
                await title.finish("未填写头衔名称 或 不能含有@全体成员")
    else:
        await title.send(f"功能处于关闭状态，发送【开关管理】开启")


title_ = on_command('删头衔', permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER, priority=1, block=True)


@title_.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    """
    /删头衔 @user 删除头衔
    """
    msg = str(event.get_message())
    stitle = msg.split()[-1:][0]
    logger.info(str(msg.split()), stitle)
    sb = At(event.json())
    gid = event.group_id
    status = await check_func_status("admin", str(gid))
    if status:
        if sb:
            if 'all' not in sb:
                try:
                    for qq in sb:
                        await bot.set_group_special_title(
                            group_id=gid,
                            user_id=int(qq),
                            special_title="",
                            duration=-1,
                        )
                except ActionFailed:
                    await title_.finish("权限不足")
                else:
                    logger.info(f"改头衔操作成功{stitle}")
                    if cb_notice:
                        await title_.finish(f"改头衔操作成功{stitle}")
            else:
                await title_.finish("有什么输入错误 或 不能含有@全体成员")
    else:
        await title_.send(f"功能处于关闭状态，发送【开关管理】开启")


kick = on_command('踢', permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER, priority=1, block=True)


@kick.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    """
    /踢 @user 踢出某人
    """
    msg = str(event.get_message())
    sb = At(event.json())
    gid = event.group_id
    status = await check_func_status("admin", str(gid))
    if status:
        if sb:
            if 'all' not in sb:
                try:
                    for qq in sb:
                        await bot.set_group_kick(
                            group_id=gid,
                            user_id=int(qq),
                            reject_add_request=False
                        )
                except ActionFailed:
                    await kick.finish("权限不足")
                else:
                    logger.info(f"踢人操作成功")
                    if cb_notice:
                        await kick.finish(f"踢人操作成功")
            else:
                await kick.finish("不能含有@全体成员")
    else:
        await kick.send(f"功能处于关闭状态，发送【开关管理】开启")


kick_ = on_command('黑', permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER, priority=1, block=True)


@kick_.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    """
    黑 @user 踢出并拉黑某人
    """
    msg = str(event.get_message())
    sb = At(event.json())
    gid = event.group_id
    status = await check_func_status("admin", str(gid))
    if status:
        if sb:
            if 'all' not in sb:
                try:
                    for qq in sb:
                        await bot.set_group_kick(
                            group_id=gid,
                            user_id=int(qq),
                            reject_add_request=True
                        )
                except ActionFailed:
                    await kick_.finish("权限不足")
                else:
                    logger.info(f"踢人并拉黑操作成功")
                    if cb_notice:
                        await kick_.finish(f"踢人并拉黑操作成功")
            else:
                await kick_.finish("不能含有@全体成员")
    else:
        await kick_.send(f"功能处于关闭状态，发送【开关管理】开启")


set_g_admin = on_command("管理员+", permission=SUPERUSER | GROUP_OWNER, priority=1, block=True)


@set_g_admin.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    """
    管理员+ @user 添加群管理员
    """
    msg = str(event.get_message())
    logger.info(msg)
    logger.info(msg.split())
    sb = At(event.json())
    logger.info(sb)
    gid = event.group_id
    status = await check_func_status("admin", str(gid))
    if status:
        if sb:
            if 'all' not in sb:
                try:
                    for qq in sb:
                        await bot.set_group_admin(
                            group_id=gid,
                            user_id=int(qq),
                            enable=True
                        )
                except ActionFailed:
                    await set_g_admin.finish("权限不足")
                else:
                    logger.info(f"设置管理员操作成功")
                    await set_g_admin.finish("设置管理员操作成功")
            else:
                await set_g_admin.finish("指令不正确 或 不能含有@全体成员")
    else:
        await set_g_admin.send(f"功能处于关闭状态，发送【开关管理】开启")


unset_g_admin = on_command("管理员-", permission=SUPERUSER | GROUP_OWNER, priority=1, block=True)


@unset_g_admin.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    """
    管理员+ @user 添加群管理员
    """
    msg = str(event.get_message())
    logger.info(msg)
    logger.info(msg.split())
    sb = At(event.json())
    logger.info(sb)
    gid = event.group_id
    status = await check_func_status("admin", str(gid))
    if status:
        if sb:
            if 'all' not in sb:
                try:
                    for qq in sb:
                        await bot.set_group_admin(
                            group_id=gid,
                            user_id=int(qq),
                            enable=False
                        )
                except ActionFailed:
                    await unset_g_admin.finish("权限不足")
                else:
                    logger.info(f"取消管理员操作成功")
                    await unset_g_admin.finish("取消管理员操作成功")
            else:
                await unset_g_admin.finish("指令不正确 或 不能含有@全体成员")
    else:
        await unset_g_admin.send(f"功能处于关闭状态，发送【开关管理】开启")


msg_recall = on_command("撤回", priority=1, aliases={"删除", "recall"}, block=True,
                        permission=SUPERUSER | GROUP_ADMIN | GROUP_OWNER)


@msg_recall.handle()
async def _(bot: Bot, event: GroupMessageEvent):  # by: @tom-snow
    """
    指令格式:
    /撤回 @user n
    回复指定消息时撤回该条消息；使用艾特时撤回被艾特的人在本群 n*19 历史消息内的所有消息。
    不输入 n 则默认 n=5
    """
    # msg = str(event.get_message())
    msg = MsgText(event.json())
    sb = At(event.json())
    rp = Reply(event.json())
    gid = event.group_id
    status = await check_func_status("admin", str(gid))
    if not status:
        await msg_recall.finish("功能处于关闭状态，发送【开关管理】开启")

    if not gid:  # FIXME: 有必要加吗？
        await msg_recall.finish("请在群内使用！")

    recall_msg_id = []
    if rp:
        recall_msg_id.append(rp["message_id"])
    elif sb:
        seq = None
        if len(msg.split(" ")) > 1:
            try:  # counts = n
                counts = int(msg.split(" ")[-1])
            except ValueError:
                counts = 5  # 出现错误就默认为 5 【理论上除非是 /撤回 @user n 且 n 不是数值时才有可能触发】
        else:
            counts = 5

        try:
            for i in range(counts):  # 获取 n 次
                await asleep(randint(0, 10))  # 睡眠随机时间，避免黑号
                res = await bot.call_api("get_group_msg_history", group_id=gid, message_seq=seq)  # 获取历史消息
                flag = True
                for message in res["messages"]:  # 历史消息列表
                    if flag:
                        seq = int(message["message_seq"]) - 1
                        flag = False
                    if int(message["user_id"]) in sb:  # 将消息id加入列表
                        recall_msg_id.append(int(message["message_id"]))
        except ActionFailed as e:
            await msg_recall.send(f"获取群历史消息时发生错误")
            logger.error(f"获取群历史消息时发生错误：{e}, seq: {seq}")
            print_exc()
    else:
        await msg_recall.finish("指令格式：\n/撤回 @user n\n回复指定消息时撤回该条消息；使用艾特时撤回被艾特的人在本群 n*19 历史消息内的所有消息。\n不输入 n 则默认 n=5")

    # 实际进行撤回的部分
    try:
        for msg_id in recall_msg_id:
            await asleep(randint(0, 3))  # 睡眠随机时间，避免黑号
            await bot.call_api("delete_msg", message_id=msg_id)
    except ActionFailed as e:
        logger.warning(f"执行失败，可能是我权限不足 {e}")
        await msg_recall.finish("执行失败，可能是我权限不足")
    else:
        logger.info(f"操作成功，一共撤回了 {len(recall_msg_id)} 条消息")
        if cb_notice:
            await msg_recall.finish(f"操作成功，一共撤回了 {len(recall_msg_id)} 条消息")


"""
! 消息防撤回模块，默认不开启，有需要的自行开启，想对部分群生效也需自行实现(可以并入本插件的开关系统内，也可控制 go-cqhttp 的事件过滤器)

如果在 go-cqhttp 开启了事件过滤器，请确保允许 post_type=notice 通行
【至少也得允许 notice_type=group_recall 通行】
"""
async def _group_recall(bot: Bot, event: NoticeEvent)->bool:
    # 有需要自行取消注释
    # if event.notice_type == 'group_recall':
    #     return True
    return False

group_recall = on_notice(_group_recall, priority=5)

@group_recall.handle()
async def _(bot: Bot, event: NoticeEvent):
    event_obj = json.loads(event.json())
    user_id = event_obj["user_id"] # 消息发送者
    operator_id = event_obj["operator_id"] # 撤回消息的人
    group_id = event_obj["group_id"] # 群号
    message_id = event_obj["message_id"] # 消息 id

    if int(user_id) != int(operator_id): return # 撤回人不是发消息人，是管理员撤回成员消息，不处理
    if int(operator_id) in su or str(operator_id) in su: return # 发起撤回的人是超管，不处理
    # 管理员撤回自己的也不处理
    operator_info = await bot.get_group_member_info(group_id=group_id, user_id=operator_id, no_cache=True)
    if operator_info["role"] != "member": return
    # 防撤回
    recalled_message = await bot.get_msg(message_id=message_id)
    recall_notice = f"检测到{ operator_info['card'] if operator_info['card'] else operator_info['nickname'] }({ operator_info['user_id'] })撤回了一条消息：\n\n"
    await bot.send_group_msg(group_id=group_id, message=recall_notice + recalled_message['message'])
    await group_recall.finish()