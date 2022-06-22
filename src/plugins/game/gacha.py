#!/usr/bin/python
# -*- coding: UTF-8 -*-
import random
from nonebot import on_command, on_regex
from nonebot.rule import to_me
from nonebot.params import State, CommandArg
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message
from .utils import *
from .data_source import isInService
try:
    import ujson as json
except ModuleNotFoundError:
    import json


ck_player = {}


class NormalData:
    sixList = []

    fiveList = []

    fourList = []

    threeList = []

    onelist = ['虾虾']

    fiveListUp = []
    sixListUP = []


def singleDrawing(event: GroupMessageEvent):
        global ck_player, player_data

        ck_user_id = ck_player[event.group_id][1]
        ck_user_id = str(ck_user_id)
        group_id = event.group_id
        group_id = str(group_id)

        randomResult = random.randint(1, 10000)
        if randomResult <= 10:
            player_data[group_id][ck_user_id]['num1'] += 1
            return '★——' + NormalData().onelist[0]
        elif randomResult <= 200:
            player_data[group_id][ck_user_id]['num6'] += 1
            randomResult = random.randint(1, 10000)
            if randomResult <= 5000:
                return '【★★★★★★UP!】——' + NormalData().sixListUp[random.randint(0, 1)]
            else:
                a = NormalData().sixList.index(max(NormalData().sixList))
                return '【★★★★★★】——' + NormalData().sixList[random.randint(0, a)]
        elif randomResult <= 1000:
            player_data[group_id][ck_user_id]['num5'] += 1
            randomResult = random.randint(1, 10000)
            if randomResult <= 5000:
                return '[★★★★★UP!]——' + NormalData().fiveListUp[random.randint(0, 1)]
            else:
                a = NormalData().fiveList.index(max(NormalData().fiveList))
                return '[★★★★★]——' + NormalData().fiveList[random.randint(0, a)]
        elif randomResult <= 6000:
            player_data[group_id][ck_user_id]['num4'] += 1
            a = NormalData().fourList.index(max(NormalData().fourList))
            return '☆☆☆☆——' + NormalData().fourList[random.randint(0, a)]
        else:
            player_data[group_id][ck_user_id]['num3'] += 1
            a = NormalData().threeList.index(max(NormalData().threeList))
            return '☆☆☆——' + NormalData().threeList[random.randint(0, a)]


one = on_command('抽卡', 
                aliases={'单抽'}, 
                rule=to_me() & isInService("抽卡", 1), 
                priority=5)
@one.handle()
async def arkRandom(bot: Bot, event: GroupMessageEvent, state: T_State = State()):
    ids = event.get_session_id()
    _, group_id, user_id = event.get_session_id().split("_")
    
    global player_data, ck_player
    player_is_exists(event)
    money = state['money'] = 100
    user_money = player_data[str(event.group_id)][str(event.user_id)]['gold']
    if money > user_money:
        await one.finish('你现在没有钱，抽不起卡啦！\n【首次游玩请发送 [签到] 来获取金币】', at_sender=True)
        
    num6 = player_data[str(event.group_id)][str(event.user_id)]['num6']
    num5 = player_data[str(event.group_id)][str(event.user_id)]['num5']
    num4 = player_data[str(event.group_id)][str(event.user_id)]['num4']
    num3 = player_data[str(event.group_id)][str(event.user_id)]['num3']
    num1 = player_data[str(event.group_id)][str(event.user_id)]['num1']

    user_name = event.sender.card if event.sender.nickname else event.sender.nickname
    ck_player[event.group_id] = {1: event.user_id,
                                'money': money,
                                'num6': num6,
                                'num5': num5,
                                'num4': num4,
                                'num3': num3,
                                'num1': num1}

    gold = ck_player[event.group_id]['money']
    ck_user_id = ck_player[event.group_id][1]
    ck_user_id = str(ck_user_id)
    group_id = event.group_id
    group_id = str(group_id)
    player_data[group_id][ck_user_id]['gold'] -= gold

    own_gold = player_data[str(event.group_id)][str(event.user_id)]['gold']
    msg = user_name + ' 抽到了: \n' + singleDrawing(event) + f'\n\n本次抽卡花费100金币\n你还有 {own_gold} 金币'
    await bot.send(event=event, message=msg)
    ck_player[event.group_id] = {}
    with open(file, 'w', encoding='utf8') as f:
        json.dump(player_data, f, ensure_ascii=False, indent=4)



ten = on_command('十连', 
                rule=to_me() & isInService("抽卡", 1), 
                priority=5)
@ten.handle()
async def arkRandomTen(bot: Bot, event: GroupMessageEvent, state: T_State = State()):
    ids = event.get_session_id()
    _, group_id, user_id = event.get_session_id().split("_")

    global player_data, ck_player
    player_is_exists(event)
    money = state['money'] = 1000
    user_money = player_data[str(event.group_id)][str(event.user_id)]['gold']
    if money > user_money:
        await one.finish('你现在没有钱，抽不起卡啦！\n【首次游玩请发送 [签到] 来获取金币】', at_sender=True)

    num6 = player_data[str(event.group_id)][str(event.user_id)]['num6']
    num5 = player_data[str(event.group_id)][str(event.user_id)]['num5']
    num4 = player_data[str(event.group_id)][str(event.user_id)]['num4']
    num3 = player_data[str(event.group_id)][str(event.user_id)]['num3']
    num1 = player_data[str(event.group_id)][str(event.user_id)]['num1']

    user_name = event.sender.card if event.sender.nickname else event.sender.nickname
    ck_player[event.group_id] = {1: event.user_id,
                                'money': money,
                                'num6': num6,
                                'num5': num5,
                                'num4': num4,
                                'num3': num3,
                                'num1': num1}

    gold = ck_player[event.group_id]['money']
    ck_user_id = ck_player[event.group_id][1]
    ck_user_id = str(ck_user_id)
    group_id = event.group_id
    group_id = str(group_id)
    player_data[group_id][ck_user_id]['gold'] -= gold

    own_gold = player_data[str(event.group_id)][str(event.user_id)]['gold']
    msg = (user_name + ' 的十连结果：\n' + singleDrawing(event) + '\n' +
            singleDrawing(event) + '\n' + singleDrawing(event) + '\n' +
            singleDrawing(event) + '\n' + singleDrawing(event) + '\n' +
            singleDrawing(event) + '\n' + singleDrawing(event) + '\n' +
            singleDrawing(event) + '\n' + singleDrawing(event) + '\n' +
            singleDrawing(event) + f'\n\n本次抽卡花费1000金币\n你还有 {own_gold} 金币')
    await bot.send(event=event, message=msg)
    ck_player[event.group_id] = {}
    with open(file, 'w', encoding='utf8') as f:
        json.dump(player_data, f, ensure_ascii=False, indent=4)


possibility = on_command('卡池', 
                        rule=to_me() & isInService("抽卡", 1), 
                        priority=5)
@possibility.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State = State(), text: Message = CommandArg):
    args = text.extract_plain_text()
    if args: 
        state["list"] = args

@possibility.got("list", prompt="想要查看几星（或up）的列表？")
async def _(bot: Bot, event: GroupMessageEvent, state: T_State = State()):
    msg = state["list"]

    list6 = str(NormalData().sixList).replace('[', '').replace(']', '').replace(',', '；').replace("'", '')
    list6up = str(NormalData().sixListUp).replace('[', '').replace(']', '').replace(',', '；').replace("'", '')
    list5 = str(NormalData().fiveList).replace('[', '').replace(']', '').replace(',', '；').replace("'", '')
    list5up = str(NormalData().fiveListUp).replace('[', '').replace(']', '').replace(',', '；').replace("'", '')
    list4 = str(NormalData().fourList).replace('[', '').replace(']', '').replace(',', '；').replace("'", '')
    list3 = str(NormalData().threeList).replace('[', '').replace(']', '').replace(',', '；').replace("'", '')
    number6 = len(NormalData().sixList) + len(NormalData().sixListUp)
    number5 = len(NormalData().fiveList) + len(NormalData().fiveListUp)
    number4 = len(NormalData().fourList)
    number3 = len(NormalData().threeList)
    number = number6 + number5 + number4 + number3 + 1

    if '全部' in msg:
        await possibility.finish(f'卡池目前一共有 {number} 个角色\n\n六星：共 {number6} 个\n' + list6 + '\n概率UP角色为：' + list6up
                + f'\n\n五星：共 {number5} 个\n' + list5 + '\n概率UP角色为：' + list5up
                + f'\n\n四星：共 {number4} 个\n' + list4
                + f'\n\n三星：共 {number3} 个\n' + list3 + '\n\n一星只有一个：那便是作为邪神祭品的 虾虾 ！')
    elif '六' in msg:
        await possibility.finish(f'六星：共 {number6} 个\n' + list6 + '\n概率UP角色为：' + list6up)
    elif '五' in msg:
        await possibility.finish(f'五星：共 {number5} 个\n' + list5 + '\n概率UP角色为：' + list5up)
    elif '四' in msg:
        await possibility.finish(f'四星：共 {number4} 个\n' + list4)
    elif '三' in msg:
        await possibility.finish(f'三星：共 {number3} 个\n' + list3)
    elif '一' in msg:
        await possibility.finish('一星只有一个：那便是作为邪神祭品的 虾虾 ！')
    elif 'up' in msg:
        await possibility.finish(f'现在UP的角色为：\n六星：' + list6up + '\n五星：' + list5up)
    else:
        await possibility.finish('没有该稀有度，或者用汉字取代阿拉伯数字')


sell = on_regex('售卖(.*?)[个](.*?)星',
                rule=isInService("抽卡", 1),
                priority=5)
@sell.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State = State()):
    player_is_exists(event)
    info = state["_matched_groups"]
    info = list(info)
    if info[0]:
        try:
            amount = int(info[0])
        except:
            await sell.finish('能不能用数字？')

    if info[1]:
        info[1] = str(info[1]).replace('一', '1').replace('二', '2').replace('三', '3').replace('四', '4').replace('五', '5').replace('六', '6')
        info[1] = int(info[1])
        if info[1] >= 6:
            await sell.finish('六星或以上无法售卖')
        elif info[1] <= 2:
            await sell.finish('二星或以下无法售卖')
        
        if info[1] == 3:
            num = 'num3'
            cost = 25
            a = '三'
        elif info[1] == 4:
            num = 'num4'
            cost = 50
            a = '四'
        elif info[1] == 5:
            num = 'num5'
            cost = 250
            a = '五'
        star = player_data[str(event.group_id)][str(event.user_id)][f'{num}']
        if amount > star:
            await sell.finish('售卖的数量大于你拥有的数量')
        cost = amount * cost
        player_data[str(event.group_id)][str(event.user_id)][f'{num}'] -= amount
        player_data[str(event.group_id)][str(event.user_id)]['gold'] += cost
        number = player_data[str(event.group_id)][str(event.user_id)][f'{num}']
        gold = player_data[str(event.group_id)][str(event.user_id)]['gold']
        await sell.send(dates() + f'你售卖了 {amount} 个{a}星，获取了 {cost} 金币\n\n你现在拥有 {number} 个{a}星、{gold} 金币', at_sender=True)
        with open(file, 'w', encoding='utf8') as f:
            json.dump(player_data, f, ensure_ascii=False, indent=4)