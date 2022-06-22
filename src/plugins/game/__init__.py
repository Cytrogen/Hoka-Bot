#!/usr/bin/python
# -*- coding: UTF-8 -*-
from datetime import date
from nonebot import require
from .russian import *
from .utils import *
from .gacha import *
from .job import *
from .data_source import *


__help_plugin_name__ = '群组游戏'
__des__ = '群组游戏'
__author__ = 'HibiKier + AkashiCoin + Cytrogen'
__level__ = '1\n'
__cmd__ = '''

\n【俄罗斯轮盘】
装弹/轮盘 <子弹> <金额>
接受/拒绝
开枪
结算
我的战绩
金币/胜场/败场/欧洲人/慈善家 排行

【抽卡】
hoka 抽卡/十连
卡池 <星数/全部/UP>
我的背包
售卖 <num>个<x>星

【群职业】
hoka 签到
hoka 打工
hoka 找工作/职业 <职业>
hoka 辞职
职业信息 <职业>
我的职业\n
'''.strip()
__example__ = '''

\n装弹 6 200
售卖69个三星
hoka职业爱豆
\n
'''.strip()
__note__ = '''
- N/A'''
__usage__ = f'''{__des__}
作者：{__author__}
权限等级：{__level__}
用法：{__cmd__}
举例：{__example__}
备注：{__note__}'''


sign = on_command('签到', 
                rule=to_me() & isInService("金币获取", 1), 
                permission=GROUP, 
                priority=5, 
                block=True)
@sign.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State = State()):
    global player_data

    rnd = random.Random()
    rnd.seed((int(date.today().strftime("%y%m%d")) * 45) * (int(event.get_user_id()) * 55))
    lucknum = rnd.randint(1, 100)
    gold = rnd.randint(100,500)

    player_is_exists(event)
    if player_data[str(event.group_id)][str(event.user_id)]['is_sign']:
        await sign.finish(random.choice([f'\n你已经签到过了！',
                '\n拿了钱就不可以再拿了！',
                '\nhoka知道你今天已经签过了！']) + 
                f'\n你今天获得了 {gold} 金币\n幸运指数是 {lucknum}\n抽到的签为“{luck_simple(lucknum)}”', at_sender=True)
    
    await sign.send(f'\n签到成功！\n你获得了 {gold} 金币' + 
            f'\n你的幸运指数是 {lucknum}\n抽到的签为“{luck_simple(lucknum)}”\n', at_sender=True)
    player_data[str(event.group_id)][str(event.user_id)]['gold'] += gold
    player_data[str(event.group_id)][str(event.user_id)]['make_gold'] += gold
    player_data[str(event.group_id)][str(event.user_id)]['is_sign'] = True
    with open(file, 'w', encoding='utf8') as f:
        json.dump(player_data, f, ensure_ascii=False, indent=4)


work = on_command('打工', 
                rule=to_me() & isInService("金币获取", 1), 
                permission=GROUP,
                priority=5, 
                block=True)
@work.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State = State(), text: Message = CommandArg()):
    global player_data

    player_is_exists(event)
    if player_data[str(event.group_id)][str(event.user_id)]['job'] == 1:
        await work.finish("你现在是职业爱豆！无法打工！", at_sender=True)

    if player_data[str(event.group_id)][str(event.user_id)]['is_work']:
        if player_data[str(event.group_id)][str(event.user_id)]['num1'] >= 1:
            shrimp = player_data[str(event.group_id)][str(event.user_id)]['num1']
            user_name = event.sender.card if event.sender.nickname else event.sender.nickname
            await work.send(f"{user_name} 将一只虾虾献祭给了肖战邪神——堂堂的万圣节恶魔！\n邪神很满意，赋予了你一次可能会猝死的打工机会\n\n你还剩{shrimp}只虾虾")
            player_data[str(event.group_id)][str(event.user_id)]['is_work'] = False
            player_data[str(event.group_id)][str(event.user_id)]['num1'] -= 1
        else:
            await work.finish(random.choice([f'\n你已经打过工了！', '\n打工还想卷？爬！', '\nhoka知道你今天已经打过工了！']), at_sender=True)

    args = text.extract_plain_text()
    if args:
        state["type"] = args

@work.got("type", prompt="现在可以打的工为：\n毁灭世界\n考美院\n当水军")
async def handle_city(bot: Bot, event: GroupMessageEvent, state: T_State = State()):
    job = state["type"]

    rnd = random.Random()
    gold = rnd.randint(250,600)
    get_gold = False
    a = random.randint(1, 10)

    if '毁灭' in job:
        weapon = random.choice(['飞侠炸弹', '草莓小笼包', '菠萝麻婆豆腐', '兰州不许吃肉面', '湿婆河水飞饼', '川宝FAKE NEWS鸡翅', '仰望星之彩派',
                    '瑞典鲑鱼叉烧饭', '纳豆拌饭', '拜登椅子', '玉米加农炮', 'NTR黄油'])
        if a == 1:
            events = dates() + random.choice([f'你研制出了生化武器 {weapon}，并卖给hoka帮助他毁灭世界\nhoka没感觉到这东西有什么用，没给你钱',
                    f'你将自己研究出的杀伤性武器 {weapon} 卖给了hoka\n但hoka没付你钱',
                    f'猫猫联盟要求你制作灭狗喷雾，你虽然没做出来但却研究出了 {weapon}\n可恶的猫猫对你使用了 {weapon}，然后逃了单',
                    f'你使用了 {weapon} 随机攻击一位幸运路人，该路人被你残忍杀害\n邪神吃完路人，没给钱就走了',
                    f'{weapon} 被你恶意散播在街道上，大家都被你气晕\n你尝试搜刮路人的钱包，但他们也都是穷狗'])
        else:
            get_gold = True
            events = dates() + random.choice([f'你研制出了生化武器 {weapon}，并卖给hoka帮助他毁灭世界\nhoka很开心，给了你 {gold} 金币',
                    f'你将自己研究出的杀伤性武器 {weapon} 卖给了hoka\nhoka付给了你 {gold} 金币',
                    f'猫猫联盟要求你制作灭狗喷雾，你虽然没做出来但却研究出了 {weapon}\n猫猫联盟很满意，给你了 {gold} 金币',
                    f'你使用了 {weapon} 随机攻击一位幸运路人，该路人被你残忍杀害\n邪神很高兴，支付了你 {gold} 金币',
                    f'{weapon} 被你恶意散播在街道上，大家都被你气晕\n你靠着搜刮路人钱包得到了 {gold} 金币'])
    elif '美院' in job:
        if a == 1:
            events = dates() + random.choice(['你想考入美院，却落榜了\n和所有落榜生一样，你被大众遗忘',
                    '考美院的时候你惨遭落选\n美院对外表示是你自己不努力。你惨遭被网络数落',
                    '你成功考入美院，却在食堂内被学姐诬陷摸了她的腚\n你最终靠监控还了自己清白，对方道歉一声该事便没了后续',
                    '可惜，你落选了。不过你并没有因此而放弃\n你选择重振国家，发动了250战\n最终你被围殴，不得不停战自闭'])
        else:
            get_gold = True
            events = dates() + random.choice([f'你想考入美院，却落榜了\n欧联听后抓紧给了你 {gold} 金币',
                    f'考美院的时候你惨遭落选\n美院支付了你 {gold} 金币作为精神损失费',
                    f'你成功考入美院，却在食堂内被学姐诬陷摸了她的腚\n你最终靠监控还了自己清白，并声称自己是穆斯林变性人，对方不得不支付你 {gold} 金币作为补偿',
                    f'可惜，你落选了。不过你并没有因此而放弃\n你选择重振国家，发动了250战\n最终你战胜了美院，得到了 {gold} 金币'])
    elif '水军' in job:
        if player_data[str(event.group_id)][str(event.user_id)]['job'] == 2:
            await work.finish("你是传教士，无法做水军！")
        company = random.choice(['企鹅', '面条哈游', '老王易'])
        company2 = random.choice(['南极贱畜', '糯米哈游', '网不易'])
        indivi = random.choice(['hoka', 'null', 'QQ小冰'])
        if a == 1:
            events = dates() + random.choice([f'你为 {company} 做水军，诬陷 {company2} 的新游戏\n你做得不大行，{company} 不打算付你钱',
                    f'你为 {company} 做水军，诬陷 {company2} 的新游戏\n你做得稀烂，被网友发现你是水军\n你什么也没得到',
                    f'{company} 要求你作为托捧他家的新游戏\n你照做了，但没有任何节奏被掀起，也没有任何金币支付给你',
                    f'你为 {company2} 做水军，诬陷 {company} 的新游戏\n你做得很不好，{company2} 什么也没给你',
                    f'虾虾们找到你，想要你在微波上多赞美些肖战邪神\n你被网友围殴后又被虾虾们开除了粉籍，你什么都没得到',
                    f'{indivi} 的管理员大量招募水军，你便是其中一员\n你在贴吗内宣传了他的bot，他却不给钱'])
        else:
            get_gold = True
            events = dates() + random.choice([f'你为 {company} 做水军，诬陷 {company2} 的新游戏\n你做得很好，{company} 支付了你 {gold} 金币',
                    f'你为 {company} 做水军，诬陷 {company2} 的新游戏\n你做得稀烂，被网友发现你是水军\n但反转了，{company2} 反而支付了你 {gold} 金币',
                    f'{company} 要求你作为托捧他家的新游戏\n你照做了，虽然评论区都在骂你狗托，但 {gold} 金币还是打在了你卡上',
                    f'你为 {company2} 做水军，诬陷 {company} 的新游戏\n你做得不错，{company2} 支付了你 {gold} 金币',
                    f'虾虾们找到你，想要你在微波上多赞美些肖战邪神\n你有些不情愿，但 {gold} 金币太香了',
                    f'{indivi} 的管理员大量招募水军，你便是其中一员\n你在贴吗内宣传了他的bot，他给了你 {gold} 金币'])
    else:
        await work.finish('该工作不是可选项')

    await work.send(events, at_sender=True)
    if get_gold:
        player_data[str(event.group_id)][str(event.user_id)]['gold'] += gold
        player_data[str(event.group_id)][str(event.user_id)]['make_gold'] += gold
        player_data[str(event.group_id)][str(event.user_id)]['is_work'] = True
        with open(file, 'w', encoding='utf8') as f:
            json.dump(player_data, f, ensure_ascii=False, indent=4)


record = on_command('我的战绩', 
                    permission=GROUP,
                    rule=isInService("俄罗斯轮盘", 1),
                    priority=5, 
                    block=True)
@record.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State = State()):
    global player_data
    player_is_exists(event)
    user = player_data[str(event.group_id)][str(event.user_id)]
    await record.send(f'游戏战绩\n'
                      f'胜利场次：{user["win_count"]}\n'
                      f'失败场次：{user["lose_count"]}\n'
                      f'赚取金币：{user["make_gold"]}\n'
                      f'输掉金币：{user["lose_gold"]}', at_sender=True)


game_rank = on_command('胜场排行', 
                    aliases={'金币排行', '胜利排行', '败场排行', '失败排行','欧洲人排行', '慈善家排行'},
                    rule=isInService("俄罗斯轮盘", 1),
                    permission=GROUP, 
                    priority=5, 
                    block=True)
@game_rank.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State = State()):
    global player_data
    if state["_prefix"]["raw_command"] in ['金币排行']:
        await game_rank.finish(await rank(player_data, event.group_id, 'gold_rank'))
    if state["_prefix"]["raw_command"] in ['胜场排行', '胜利排行']:
        await game_rank.finish(await rank(player_data, event.group_id, 'win_rank'))
    if state["_prefix"]["raw_command"] in ['败场排行', '失败排行']:
        await game_rank.finish(await rank(player_data, event.group_id, 'lose_rank'))
    if state["_prefix"]["raw_command"] == '欧洲人排行':
        await game_rank.finish(await rank(player_data, event.group_id, 'make_gold'))
    if state["_prefix"]["raw_command"] == '慈善家排行':
        await game_rank.finish(await rank(player_data, event.group_id, 'lose_gold'))


my_gold = on_command('我的金币', 
                    permission=GROUP, 
                    rule=isInService("金币获取", 1),
                    priority=5, 
                    block=True)
@my_gold.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State = State()):
    global player_data
    player_is_exists(event)
    gold = player_data[str(event.group_id)][str(event.user_id)]['gold']
    await my_gold.send(f'\n你还有 {gold} 枚金币捏捏', at_sender=True)


my_bag = on_command('我的背包', 
                    permission=GROUP,
                    rule=isInService("抽卡", 1),
                    priority=5, 
                    block=True)
@my_bag.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State = State()):
    global player_data
    player_is_exists(event)
    num6 = player_data[str(event.group_id)][str(event.user_id)]['num6']
    num5 = player_data[str(event.group_id)][str(event.user_id)]['num5']
    num4 = player_data[str(event.group_id)][str(event.user_id)]['num4']
    num3 = player_data[str(event.group_id)][str(event.user_id)]['num3']
    num1 = player_data[str(event.group_id)][str(event.user_id)]['num1']
    await my_bag.finish(f'\n你一共抽到了：\n{num6}个六星\n{num5}个五星\n{num4}个四星\n{num3}个三星\n{num1}只虾虾', at_sender=True)


scheduler = require("nonebot_plugin_apscheduler").scheduler
@scheduler.scheduled_job(
    'cron',
    hour=0,
    minute=0,
)
async def _():
    global player_data
    for group in player_data.keys():
        for user_id in player_data[group].keys():
            player_data[group][user_id]['is_sign'] = False
            player_data[group][user_id]['is_work'] = False
            player_data[group][user_id]['is_belief'] = False
            player_data[group][user_id]['is_teach'] = False
            player_data[group][user_id]['is_study'] = False
            player_data[group][user_id]['is_train'] = False
            player_data[group][user_id]['is_ptt'] = False
            player_data[group][user_id]['is_lpt'] = False
            if player_data[group][user_id]['sing'] >= 1:
                player_data[group][user_id]['sing'] -= 1
            if player_data[group][user_id]['jail'] >= 1:
                player_data[group][user_id]['jail'] -= 1
                if player_data[group][user_id]['jail'] == 0:
                    player_data[group][user_id]['is_jail'] = False
            if player_data[group][user_id]['is_off'] >= 1:
                player_data[group][user_id]['is_off'] -= 1
    with open(file, 'w', encoding='utf8') as f:
        json.dump(player_data, f, ensure_ascii=False, indent=4)
    print('所有演唱会冷却时间-1')
    print('所有刑期日期-1')
    print('所有的辞职冷却时间-1')
    print('每日签到重置成功啦！赌狗快醒醒！')