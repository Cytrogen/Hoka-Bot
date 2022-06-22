#!/usr/bin/python
# -*- coding: UTF-8 -*-
import random
import asyncio
import os
import time
import nonebot
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.params import Depends, CommandArg, State
from nonebot.adapters.onebot.v11 import GROUP, Bot, GroupMessageEvent, Message, MessageSegment
from .utils import get_message_at, is_number, get_message_text, player_is_exists
from .data_source import end_handle, isInService
from pathlib import Path
try:
    import ujson as json
except ModuleNotFoundError:
    import json


driver: nonebot.Driver = nonebot.get_driver()
bot_name = list(driver.config.nickname)[0] if driver.config.nickname else 'hoka'
max_bet_gold = driver.config.max_bet_gold if driver.config.max_bet_gold else 1000
game_path = driver.config.game_path if driver.config.game_path else ''


player_data = {}
if game_path:
    file = Path(game_path) / 'game_data.json'
    file.parent.mkdir(exist_ok=True, parents=True)
    if file.exists():
        player_data = json.load(open(file, 'r', encoding='utf8'))
    else:
        old_file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'game_data.json'))
        if os.path.exists(old_file):
            os.rename(old_file, file)
            player_data = json.load(open(file, 'r', encoding='utf8'))
else:
    file = os.path.abspath(os.path.join(os.path.dirname(__file__), 'game_data.json'))
    if os.path.exists(file):
        player_data = json.load(open(file, 'r', encoding='utf8'))


async def get_bullet_num(event: GroupMessageEvent, arg: Message = CommandArg(), state: T_State = State()):
    msg = get_message_text(event.json())
    if state["bullet_num"]:
        return state
    if msg in ['取消', '算了']:
        await rssian.finish('已取消操作...')
    try:
        if rs_player[event.group_id][1] != 0:
            await rssian.finish('决斗已开始……', at_sender=True)
    except KeyError:
        pass
    if not is_number(msg):
        await rssian.reject('输入子弹数量必须是数字啊喂！')
    if int(msg) < 1 or int(msg) > 6:
        await rssian.reject('子弹数量必须大于0小于7！')
    state['bullet_num'] = int(msg)


rs_player = {}
rssian = on_command('装弹', 
                    aliases={'轮盘'},
                    rule=isInService("俄罗斯轮盘", 1),
                    permission=GROUP, 
                    priority=5, 
                    block=True)
@rssian.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State = State()):
    global rs_player
    player_is_exists(event)
    msg = get_message_text(event.json())
    try:
        if rs_player[event.group_id][1] and not rs_player[event.group_id][2] and \
                time.time() - rs_player[event.group_id]['time'] <= 60:
            await rssian.finish(f'现在是 {rs_player[event.group_id]["player1"]} 发起的对决\n请等待比赛结束后再开始下一轮……')
        if rs_player[event.group_id][1] and rs_player[event.group_id][2] and \
                time.time() - rs_player[event.group_id]['time'] <= 60:
            await rssian.finish(f'{rs_player[event.group_id]["player1"]} 和'
                                f' {rs_player[event.group_id]["player2"]}的对决还未结束！')
        if rs_player[event.group_id][1] and rs_player[event.group_id][2] and \
                time.time() - rs_player[event.group_id]['time'] > 60:
            await rssian.send('决斗已过时，强行结算了捏')
            await end_game(bot, event)
        if not rs_player[event.group_id][2] and time.time() - rs_player[event.group_id]['time'] > 60:
            rs_player[event.group_id][1] = 0
            rs_player[event.group_id][2] = 0
            rs_player[event.group_id]['at'] = 0
    except KeyError:
        pass
    if msg:
        msg = msg.split(' ')
        if len(msg) == 1:
            msg = msg[0]
            if is_number(msg) and not (int(msg) < 1 or int(msg) > 6):
                state['bullet_num'] = int(msg)
        else:
            money = msg[1].strip()
            msg = msg[0].strip()
            if is_number(msg) and not (int(msg) < 1 or int(msg) > 6):
                state['bullet_num'] = int(msg)
            if is_number(money) and 0 < int(money) <= max_bet_gold:
                state['money'] = int(money)
    state['at'] = get_message_at(event.json())

@rssian.got("bullet_num", prompt='请输入装填子弹的数量！(最多6颗)')
async def _(bot: Bot, event: GroupMessageEvent, state: T_State = Depends(get_bullet_num)):
    global rs_player, player_data
    player_is_exists(event)
    bullet_num = state['bullet_num']
    at_ = state['at']
    money = state['money'] if state.get('money') else 200
    user_money = player_data[str(event.group_id)][str(event.user_id)]['gold']
    if bullet_num < 0 or bullet_num > 6:
        await rssian.reject('子弹数量必须大于0小于7！速速重新装弹！')
    if money > max_bet_gold:
        await rssian.finish(f'太多了！赌狗必死！单次金额不能超过{max_bet_gold}！', at_sender=True)
    if money > user_money:
        await rssian.finish('你现在没有钱，玩不了了啦！\n【首次游玩请发送 [签到] 来获取金币】', at_sender=True)

    player1_name = event.sender.card if event.sender.nickname else event.sender.nickname

    if at_:
        at_ = at_[0]
        at_player_name = await bot.get_group_member_info(group_id=event.group_id, user_id=int(at_))
        at_player_name = at_player_name['card'] if at_player_name['card'] else at_player_name['nickname']
        msg = f'{player1_name} 向 {MessageSegment.at(at_)} 发起了决斗！请 {at_player_name} 在60秒内回复 [接受] or [拒绝]，超时此次决斗作废！'
    else:
        at_ = 0
        msg = '若60秒内无人接受挑战则此次对决作废\n【首次游玩请发送 [轮盘帮助] 来查看命令捏】'

    rs_player[event.group_id] = {1: event.user_id,
                                 'player1': player1_name,
                                 2: 0,
                                 'player2': '',
                                 'at': at_,
                                 'next': event.user_id,
                                 'money': money,
                                 'bullet': random_bullet(bullet_num),
                                 'bullet_num': bullet_num,
                                 'null_bullet_num': 7 - bullet_num,
                                 'index': 0,
                                 'time': time.time()}

    await rssian.send(Message(('咔 ' * bullet_num)[:-1] + f'，装填完毕\n挑战金额：{money}\n'
                                                         f'第一枪的概率为：{str(float(bullet_num) / 7.0 * 100)[:5]}%\n'
                                                         f'{msg}'))


accept = on_command('接受', 
                    aliases={'接受决斗', '接受挑战', '接受对决'}, 
                    permission=GROUP, 
                    rule=isInService("俄罗斯轮盘", 1),
                    priority=5, 
                    block=True)
@accept.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State = State()):
    global rs_player, player_data
    player_is_exists(event)
    try:
        if rs_player[event.group_id][1] == 0:
            await accept.finish('目前没有发起对决，你接受个勾八', at_sender=True)
    except KeyError:
        await accept.finish('目前没有进行的决斗，速速打架', at_sender=True)
    if rs_player[event.group_id][2] != 0:
        if rs_player[event.group_id][1] == event.user_id or rs_player[event.group_id][2] == event.user_id:
            await accept.finish(f'你丫的已经身处决斗之中了啊', at_sender=True)
        else:
            await accept.finish('已经有人接受对决了，给我乖乖等着', at_sender=True)
    if rs_player[event.group_id][1] == event.user_id:
        await accept.finish('你要枪毙自己，hoka于心不忍……', at_sender=True)
    if rs_player[event.group_id]['at'] != 0 and rs_player[event.group_id]['at'] != event.user_id:
        await accept.finish(Message(f'这场对决是邀请 {MessageSegment.at(rs_player[event.group_id]["at"])}的，不要捣乱！'),
                            at_sender=True)
    if time.time() - rs_player[event.group_id]['time'] > 60:
        rs_player[event.group_id] = {}
        await accept.finish('这场对决邀请已经过时了，请重新发起决斗……', at_sender=True)

    user_money = player_data[str(event.group_id)][str(event.user_id)]['gold']
    if user_money < rs_player[event.group_id]['money']:
        if rs_player[event.group_id]['at'] != 0 and rs_player[event.group_id]['at'] == event.user_id:
            rs_player[event.group_id] = {}
            await accept.finish('你现在没有钱，玩不了了啦！对决还未开始便结束了……\n【首次游玩请发送 [签到] 来获取金币】', at_sender=True)
        else:
            await accept.finish('你现在没有钱，玩不了了啦！\n【首次游玩请发送 [签到] 来获取金币】', at_sender=True)

    player2_name = event.sender.card if event.sender.card else event.sender.nickname

    rs_player[event.group_id][2] = event.user_id
    rs_player[event.group_id]['player2'] = player2_name
    rs_player[event.group_id]['time'] = time.time()

    await accept.send(Message(f'{player2_name}接受了对决！\n'
                              f'请{MessageSegment.at(rs_player[event.group_id][1])}先开枪！'))


refuse = on_command('拒绝', 
                    aliases={'拒绝决斗', '拒绝挑战', '拒绝对决'}, 
                    permission=GROUP,
                    rule=isInService("俄罗斯轮盘", 1), 
                    priority=5,
                    block=True)
@refuse.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State = State()):
    global rs_player
    player_is_exists(event)
    try:
        if rs_player[event.group_id][1] == 0:
            await accept.finish('目前没有发起对决，你接受个勾八', at_sender=True)
    except KeyError:
        await refuse.finish('目前没有进行的决斗，速速打架', at_sender=True)
    if rs_player[event.group_id]['at'] != 0 and event.user_id != rs_player[event.group_id]['at']:
        await accept.finish('又不是找你决斗，你拒绝个锤子', at_sender=True)
    if rs_player[event.group_id]['at'] == event.user_id:
        at_player_name = await bot.get_group_member_info(group_id=event.group_id, user_id=event.user_id)
        at_player_name = at_player_name['card'] if at_player_name['card'] else at_player_name['nickname']
        await accept.send(Message(f'{MessageSegment.at(rs_player[event.group_id][1])}\n'
                                  f'{at_player_name}拒绝了你的对决！'))
        rs_player[event.group_id] = {}


shot = on_command('开枪', 
                aliases={'咔', '嘭', '嘣'}, 
                permission=GROUP, 
                priority=5, 
                rule=isInService("俄罗斯轮盘", 1),
                block=True)
@shot.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State = State()):
    global rs_player
    player_is_exists(event)
    try:
        if time.time() - rs_player[event.group_id]['time'] > 60:
            if rs_player[event.group_id][2] == 0:
                rs_player[event.group_id][1] = 0
                await shot.finish('这场对决已经过时了，请重新装弹吧！', at_sender=True)
            else:
                await shot.send('决斗已过时，强行结算了捏')
                await end_game(bot, event)
                return
    except KeyError:
        await shot.finish('目前没有进行的决斗，请发送 [装弹] 开启决斗吧！', at_sender=True)
    if rs_player[event.group_id][1] == 0:
        await shot.finish('没有对决，也还没装弹呢，请先输入 [装弹] 吧！', at_sender=True)
    if rs_player[event.group_id][1] == event.user_id and rs_player[event.group_id][2] == 0:
        await shot.finish('你居然要紫砂…… hoka于心不忍', at_sender=True)
    if rs_player[event.group_id][2] == 0:
        await shot.finish('请这位勇士先发送 [接受] 来站上擂台……', at_sender=True)
    player1_name = rs_player[event.group_id]['player1']
    player2_name = rs_player[event.group_id]['player2']
    if rs_player[event.group_id]['next'] != event.user_id:
        if event.user_id != rs_player[event.group_id][1] and event.user_id != rs_player[event.group_id][2]:
            nickname = event.sender.card if event.sender.card else event.sender.nickname
            await shot.finish(random.choice([
                f'不要打扰 {player1_name} 和 {player2_name} 的决斗啊！',
                '给我好好做好一个观众！hoka看到笨笨观众就会死！',
                f'不要捣乱啊笨蛋{nickname}！',
                f'讨人厌的{nickname}！不要打扰别人对决！'
            ]), at_sender=True)
        nickname = player1_name if rs_player[event.group_id]["next"] == rs_player[event.group_id][1] else player2_name
        await shot.finish(f'你家左轮连发是吧！该 {nickname} 开枪了')
    if rs_player[event.group_id]['bullet'][rs_player[event.group_id]['index']] != 1:
        await shot.send(Message(random.choice([
            '呼呼，没有爆裂的声响，你活了下来',
            '虽然黑洞洞的枪口很恐怖，但好在没有子弹射出来，你活下来了',
            '\"咔\"，你没死，看来运气不错',
            '我超，你居然没死！',
            '紧张、刺激！你开枪后居然没事！',
            '运气真好，没有子弹射出！',
            '真不错，看来你并不是美国总统'
        ]) + f'\n下一枪中弹的概率'
             f'：{str(float((rs_player[event.group_id]["bullet_num"])) / float(rs_player[event.group_id]["null_bullet_num"] - 1 + rs_player[event.group_id]["bullet_num"]) * 100)[:5]}%\n'
             f'轮到 {MessageSegment.at(rs_player[event.group_id][1] if event.user_id == rs_player[event.group_id][2] else rs_player[event.group_id][2])}了'))
        rs_player[event.group_id]["null_bullet_num"] -= 1
        rs_player[event.group_id]['next'] = rs_player[event.group_id][1] if \
            event.user_id == rs_player[event.group_id][2] else rs_player[event.group_id][2]
        rs_player[event.group_id]['time'] = time.time()
        rs_player[event.group_id]['index'] += 1
    else:
        await shot.send(random.choice([
            '\"嘭！\"，你直接去世了',
            '眼前一黑，你直接穿越到了异世界…',
            '终究还是你先走一步...',
            '笑死，你没了',
            'hoka整乐了，你紫砂成功',
            '不要随随便便就这样结束自己的生命…'
        ]) + f'\n第 {rs_player[event.group_id]["index"] + 1} 发子弹送走了你……', at_sender=True)
        win_name = player1_name if event.user_id == rs_player[event.group_id][2] else player2_name
        await asyncio.sleep(0.5)
        await shot.send(f'这场对决是 {win_name} 胜利了')
        await end_game(bot, event)


settlement = on_command('结算', 
                        permission=GROUP, 
                        rule=isInService("俄罗斯轮盘", 1),
                        priority=5, 
                        block=True)
@settlement.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State = State()):
    global rs_player
    player_is_exists(event)
    if not rs_player.get(event.group_id) or rs_player[event.group_id][1] == 0 or rs_player[event.group_id][2] == 0:
        await settlement.finish('比赛并没有开始……无法结算……', at_sender=True)
    if event.user_id != rs_player[event.group_id][1] and event.user_id != rs_player[event.group_id][2]:
        await settlement.finish('吃瓜群众不要捣乱！hoka要被你气晕了！', at_sender=True)
    if time.time() - rs_player[event.group_id]['time'] <= 60:
        await settlement.finish(f'{rs_player[event.group_id]["player1"]} 和'
                                f' {rs_player[event.group_id]["player2"]} 比赛并未超时，请继续比赛……')
    win_name = rs_player[event.group_id]["player1"] if \
        rs_player[event.group_id][2] == rs_player[event.group_id]['next'] else \
        rs_player[event.group_id]["player2"]
    await settlement.send(f'这场对决是 {win_name} 胜利了')
    await end_game(bot, event)


async def end_game(bot: Bot, event: GroupMessageEvent):
    global rs_player, player_data
    player1_name = rs_player[event.group_id]['player1']
    player2_name = rs_player[event.group_id]['player2']
    if rs_player[event.group_id]['next'] == rs_player[event.group_id][1]:
        win_user_id = rs_player[event.group_id][2]
        lose_user_id = rs_player[event.group_id][1]
        win_name = player2_name
        lose_name = player1_name
    else:
        win_user_id = rs_player[event.group_id][1]
        lose_user_id = rs_player[event.group_id][2]
        win_name = player1_name
        lose_name = player2_name
    rand = random.randint(0, 5)
    gold = rs_player[event.group_id]['money']
    fee = int(gold * float(rand) / 100)
    fee = 1 if fee < 1 and rand != 0 else fee
    player_data = end_handle(player_data, win_user_id, lose_user_id, event.group_id, gold, fee)
    win_user = player_data[str(event.group_id)][str(win_user_id)]
    lose_user = player_data[str(event.group_id)][str(lose_user_id)]
    bullet_str = ''
    for x in rs_player[event.group_id]['bullet']:
        bullet_str += '__ ' if x == 0 else '| '
    print(f'俄罗斯轮盘：胜者：{win_name} - 败者：{lose_name} - 金币：{gold}')
    await bot.send(event, message=f'【结算】\n'
                                  f'胜者：{win_name}\n'
                                  f'赢取金币：{gold - fee}\n'
                                  f'累计胜场：{win_user["win_count"]}\n'
                                  f'累计赚取金币：{win_user["make_gold"]}\n'
                                  f'-------------------\n'
                                  f'败者：{lose_name}\n'
                                  f'输掉金币：{gold}\n'
                                  f'累计败场：{lose_user["lose_count"]}\n'
                                  f'累计输掉金币：{lose_user["lose_gold"]}\n'
                                  f'-------------------\n'
                                  f'哼哼，hoka从中收取了 {float(rand)}%({fee}金币) 作为手续费！\n'
                                  f'子弹排列：{bullet_str[:-1]}')
    rs_player[event.group_id] = {}
    with open(file, 'w', encoding='utf8') as f:
        json.dump(player_data, f, ensure_ascii=False, indent=4)


def random_bullet(num: int) -> list:
    bullet_lst = [0, 0, 0, 0, 0, 0, 0]
    for i in random.sample([0, 1, 2, 3, 4, 5, 6], num):
        bullet_lst[i] = 1
    return bullet_lst