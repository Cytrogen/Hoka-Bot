import math
import random
from nonebot import on_command, require
from nonebot.permission import SUPERUSER
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from pydantic.errors import SubclassError
from .util import *
from config.config import OWNER
try:
    import ujson as json
except ModuleNotFoundError:
    import json


__info__ = '''
职业功能
["job"]：
    0：无业
    1：爱豆
    2：传教士
    3：家庭教师
'''


jb_player = {}


work = on_command("找工作", aliases={'职业'}, rule=to_me(), priority=5)
@work.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    player_is_exists(event)
    if player_data[str(event.group_id)][str(event.user_id)]['is_job']:
        await work.finish("你已经有工作了！\n你的工作为" + job_finder(), at_sender=True)

    args = str(event.get_message()).strip()
    if args:
        state["type"] = args

@work.got("type", prompt="选择你的职业：\n爱豆\n传教士\n家庭教师\n【详情可见 [职业信息]】")
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    job = state["type"]

    if '爱豆' in job:
        user_name = event.sender.card if event.sender.nickname else event.sender.nickname
        await work.send(f"{user_name} 现在是爱豆了！")
        player_data[str(event.group_id)][str(event.user_id)]['is_job'] = True
        player_data[str(event.group_id)][str(event.user_id)]['job'] = 1
    elif '传教' in job:
        user_name = event.sender.card if event.sender.nickname else event.sender.nickname
        await work.send(f"{user_name} 现在是传教士了！")
        player_data[str(event.group_id)][str(event.user_id)]['is_job'] = True
        player_data[str(event.group_id)][str(event.user_id)]['job'] = 2
    elif '教师' in job:
        user_name = event.sender.card if event.sender.nickname else event.sender.nickname
        await work.send(f"{user_name} 现在是家庭教师了！")
        player_data[str(event.group_id)][str(event.user_id)]['is_job'] = True
        player_data[str(event.group_id)][str(event.user_id)]['job'] = 3
    with open(file, 'w', encoding='utf8') as f:
        json.dump(player_data, f, ensure_ascii=False, indent=4)


quitjob = on_command("辞职", rule=to_me(), priority=5)
@quitjob.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    player_is_exists(event)
    if player_data[str(event.group_id)][str(event.user_id)]['is_job'] == False:
        await quitjob.finish("你是无业游民，你哪来的辞职一说？")
    
    player_data[str(event.group_id)][str(event.user_id)]['is_job'] = False
    player_data[str(event.group_id)][str(event.user_id)]['job'] = 0
    with open(file, 'w', encoding='utf8') as f:
        json.dump(player_data, f, ensure_ascii=False, indent=4)
    await quitjob.finish("你辞职成功，变成无业游民了！")


jobinfo = on_command("职业信息", aliases={'职业查询'}, priority=5)
@jobinfo.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["job"] = args

@jobinfo.got("job", prompt="查询哪个职业？\n无业游民\n爱豆\n传教士\n家庭教师")
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    job = state["job"]

    if '无业' in job:
        info = '无业游民：\n没有职业、只能靠打工来获取金币的人\n- 可以打所有类型的工\n- 收入不稳定，打工有概率拿不到钱'
    elif '爱豆' in job:
        info = '爱豆：\n闪闪发光的kirakira~爱抖露！\n- 无法打工\n- 依赖 [演唱会] 来获取金币\n- 演唱会的冷却为5天\n- 基于人气值获取一定比例的金币\n- 人气值可以通过每日的 [训练] 获取'
    elif '传教' in job:
        info = '传教士：\n意面教的传教士，煮不在糊传椒\n- 无法做水军，因为信仰只能有一个\n- 可以 [传教]，但煮不在糊\n- 传教有概率得到金币，或者被抓\n- 可以 [解读面经] 用快乐值来兑换金币（比例1比2）'
    elif '教师' in job:
        info = '家庭教师：\n年轻且头脑聪明的家庭教师\n- 无法打对自己有负面评价的工\n- [教学] 时需求智慧值，智慧越高获得的金币也越高\n- 可以靠 [自习] 获取智慧值'
    else:
        await jobinfo.finish("没有该职业！")
    await jobinfo.finish(info)


myjob = on_command("我的职业", aliases={'我的简历'}, priority=5)
@myjob.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    player_is_exists(event)
    user_name = event.sender.card if event.sender.nickname else event.sender.nickname
    
    job = player_data[str(event.group_id)][str(event.user_id)]['job']
    if job == 0:
        jobtype = '无业'
    elif job == 1:
        jobtype = '爱豆'
    elif job == 2:
        jobtype = '传教士'
    elif job == 3:
        jobtype = '家庭教师'
    else:
        jobtype = '错误'

    work = player_data[str(event.group_id)][str(event.user_id)]['is_work']
    belief = player_data[str(event.group_id)][str(event.user_id)]['is_belief']
    teach = player_data[str(event.group_id)][str(event.user_id)]['is_teach']
    train = player_data[str(event.group_id)][str(event.user_id)]['is_train']
    sing = player_data[str(event.group_id)][str(event.user_id)]['sing']
    study = player_data[str(event.group_id)][str(event.user_id)]['is_study']
    jail = player_data[str(event.group_id)][str(event.user_id)]['jail']
    popular = player_data[str(event.group_id)][str(event.user_id)]['popular']
    happy = player_data[str(event.group_id)][str(event.user_id)]['happy']
    wisdom = player_data[str(event.group_id)][str(event.user_id)]['wisdom']

    await myjob.finish(f'''{user_name} 的简历：
当前职业为 {jobtype}

打工：{work}
训练：{train}
传教：{belief}
教学：{teach}
演唱会还剩 {sing} 天
当前刑期为 {jail} 天
自习次数已用 {study} 次

人气值：{popular}
快乐值：{happy}
智慧值：{wisdom}''')


demon = on_command("jobfix", permission=SUPERUSER, priority=5)
@demon.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    player_is_exists(event)
    args = str(event.get_message()).strip()
    if args:
        state["value"] = args

@demon.got("value", prompt="修改哪个变量？")
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    value = state["value"]

    if '签到' in value:
        player_data[str(event.group_id)][str(event.user_id)]['is_sign'] = False
    elif '打工' in value:
        player_data[str(event.group_id)][str(event.user_id)]['is_work'] = False
    elif '传教' in value:
        player_data[str(event.group_id)][str(event.user_id)]['is_belief'] = False
    elif '监狱' in value:
        player_data[str(event.group_id)][str(event.user_id)]['is_jail'] = False
    elif '爱豆' in value:
        player_data[str(event.group_id)][str(event.user_id)]['is_work'] = False
        player_data[str(event.group_id)][str(event.user_id)]['sing'] = 0
        player_data[str(event.group_id)][str(event.user_id)]['is_train'] = False
    elif '教学' in value:
        player_data[str(event.group_id)][str(event.user_id)]['is_teach'] = False
        player_data[str(event.group_id)][str(event.user_id)]['is_study'] = 0
    with open(file, 'w', encoding='utf8') as f:
        json.dump(player_data, f, ensure_ascii=False, indent=4)
    await demon.finish("修改成功！")


demonall = on_command("alljobfix", priority=5)
@demonall.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    use = False
    ids = event.get_session_id()
    if ids.startswith("group"):
        _, group_id, user_id = event.get_session_id().split("_")
        if user_id in OWNER:
            use = True
    if use:
        player_is_exists(event)
        args = str(event.get_message()).strip()
        if args:
            state["value"] = args

@demonall.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    value = state["value"]

    if '-a' in value:
        for group in player_data.keys():
            for user_id in player_data[group].keys():
                player_data[group][user_id]['is_sign'] = False
                player_data[group][user_id]['is_work'] = False
                player_data[group][user_id]['is_belief'] = False
                player_data[group][user_id]['is_jail'] = 0
                player_data[group][user_id]['is_teach'] = False
                player_data[group][user_id]['is_study'] = 0
                player_data[group][user_id]['is_train'] = False
    elif '-c' in value:
        for user_id in player_data[str(event.group_id)].keys():
            player_data[str(event.group_id)][user_id]['is_sign'] = False
            player_data[str(event.group_id)][user_id]['is_work'] = False
            player_data[str(event.group_id)][user_id]['is_belief'] = False
            player_data[str(event.group_id)][user_id]['is_jail'] = 0
            player_data[str(event.group_id)][user_id]['is_teach'] = False
            player_data[str(event.group_id)][user_id]['is_study'] = 0
            player_data[str(event.group_id)][str(event.user_id)]['is_train'] = False
    elif '-g' in value:
        for group in player_data.keys():
            for user_id in player_data[group].keys():
                player_data[group][user_id]['gold'] += 500
    elif '-i' in value:
        for group in player_data.keys():
            for user_id in player_data[group].keys():
                player_data[group][user_id]['sing'] -= 1
    with open(file, 'w', encoding='utf8') as f:
        json.dump(player_data, f, ensure_ascii=False, indent=4)
    await demonall.finish("修改成功！")


#——————————————————————————————————————————————————————————————————————————————————————————#
### 爱豆 ###
sing = on_command("演唱会", aliases={'开演唱会'}, priority=5)
@sing.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    player_is_exists(event)
    if player_data[str(event.group_id)][str(event.user_id)]['job'] != 1:
        await sing.finish("你不是爱豆，无法开演唱会")
    if player_data[str(event.group_id)][str(event.user_id)]['sing'] >= 1:
        cool_down = player_data[str(event.group_id)][str(event.user_id)]['sing']
        await sing.finish(f"演唱会冷却时间还有 {cool_down} 天！")
    
    rnd = random.Random()
    point = rnd.randint(0, 500)
    player_data[str(event.group_id)][str(event.user_id)]['popular'] += point
    popular = player_data[str(event.group_id)][str(event.user_id)]['popular']
    gold = popular * 2
    if gold >= 7000:
        events = random.choice([f'你开了一场演唱会，观众们很狂热\n期间很顺利，你靠着演唱会获得了 {gold} 金币、{point} 人气值',
                                f'你在市中心开了一场演唱会，观众们混入了不少路人\n好在他们都被你吸引，成为了你的粉丝\n你获得了 {gold} 金币、{point} 人气值',
                                f'演唱会如期举办，你的粉丝们挤满了会场\n不出意料，你获得了 {gold} 金币、{point} 人气值'])
    elif gold >= 4500:
        events = random.choice([f'你开了一场演唱会，观众们很兴奋\n虽然气氛不是很狂热，但你还是靠着演唱会获得了 {gold} 金币、{point} 人气值',
                                f'你在市中心开了一场演唱会，观众们混入了不少路人\n这些路人们没能被你吸引\n你获得了 {gold} 金币、{point} 人气值',
                                f'演唱会如期举办，只是会场内还有些许空座\n你获得了 {gold} 金币、{point} 人气值'])
    else:
        events = random.choice([f'你开了一场演唱会，观众们很淡定\n气氛没被带起来，你靠着演唱会获得了 {gold} 金币、{point} 人气值',
                                f'你在市中心开了一场演唱会，观众里近乎都是路人\n这些路人期待的并不是你\n你获得了 {gold} 金币、{point} 人气值',
                                f'演唱会如期举办，一半的会场空荡荡的\n你获得了 {gold} 金币、{point} 人气值'])
    await sing.send(dates() + events, at_sender=True)
    player_data[str(event.group_id)][str(event.user_id)]['gold'] += gold
    player_data[str(event.group_id)][str(event.user_id)]['make_gold'] += gold
    player_data[str(event.group_id)][str(event.user_id)]['is_work'] = True
    player_data[str(event.group_id)][str(event.user_id)]['sing'] = 5
    with open(file, 'w', encoding='utf8') as f:
        json.dump(player_data, f, ensure_ascii=False, indent=4)


train = on_command("训练", aliases={"练习"}, priority=5)
@train.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    player_is_exists(event)
    if player_data[str(event.group_id)][str(event.user_id)]['job'] != 1:
        await train.finish("你不是爱豆，无法训练")
    if player_data[str(event.group_id)][str(event.user_id)]['is_train']:
        await train.finish(f"今天已经练习过了！")

    rnd = random.Random()
    point = rnd.randint(100, 350)
    player_data[str(event.group_id)][str(event.user_id)]['popular'] += point
    events = random.choice([f'你练习了一下新曲子，并上传了蓝鸟\n你获得了 {point} 人气值',
                            f'最近有个舞蹈很火，你蹭了蹭热度并上传了蓝鸟\n你获得了 {point} 人气值',
                            f'谁会不喜欢一个和观众互动的幽默爱豆呢？\n因为你在蓝鸟上一个回复，你获得了 {point} 人气值'])
    await train.send(dates() + events, at_sender=True)
    player_data[str(event.group_id)][str(event.user_id)]['is_train'] = True
    with open(file, 'w', encoding='utf8') as f:
        json.dump(player_data, f, ensure_ascii=False, indent=4)


#——————————————————————————————————————————————————————————————————————————————————————————#
### 传教士 ###
belief = on_command("传教", priority=5)
@belief.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    player_is_exists(event)
    if player_data[str(event.group_id)][str(event.user_id)]['job'] != 2:
        await sing.finish("你不是传教士，无法传教")
    if player_data[str(event.group_id)][str(event.user_id)]['is_jail']:
        if player_data[str(event.group_id)][str(event.user_id)]['jail'] == 0:
            player_data[str(event.group_id)][str(event.user_id)]['is_jail'] = False
        else:
            jail = player_data[str(event.group_id)][str(event.user_id)]['jail']
            await sing.finish(f"你在监狱里，还剩 {jail} 天释放")
    if player_data[str(event.group_id)][str(event.user_id)]['is_belief']:
        await sing.finish("今天已经传教过了！")

    rnd = random.Random()
    people = rnd.randint(1, 15)
    point = people * 17
    player_data[str(event.group_id)][str(event.user_id)]['happy'] += point
    luck = rnd.randint(1,10)
    if luck == 1:
        jail = rnd.randint(1, 3)
        events = random.choice([f'你前去宣传煮，一共有 {people} 个人信了煮\n但他们之间有个内鬼，内鬼把你抓进了监狱\n你获得了 {point} 快乐',
                                f'总共有 {people} 个人因为你而信了煮，但是警察闯了进来，你被关入了监狱\n你获得了 {point} 快乐',
                                f'煮不在糊祂多了 {people} 个信徒\n但你获取了 {point} 快乐，并且被警察抓了'])
        player_data[str(event.group_id)][str(event.user_id)]['is_jail'] = True
        player_data[str(event.group_id)][str(event.user_id)]['jail'] += jail
    elif luck <= 3:
        gold = people * 20
        events = random.choice([f'你前去宣传煮，一共有 {people} 个人信了煮\n没想到的是，一位信徒还送了你红包\n你获得了 {point} 快乐、{gold} 金币',
                                f'总共有 {people} 个人因为你而信了煮，他们为了感谢你而给了你一些金币\n你获得了 {point} 快乐、{gold} 金币',
                                f'煮不在糊祂多了 {people} 个信徒\n但你获取了 {point} 快乐、{gold} 金币'])
        player_data[str(event.group_id)][str(event.user_id)]['gold'] += gold
        player_data[str(event.group_id)][str(event.user_id)]['make_gold'] += gold
    else:
        events = random.choice([f'你前去宣传煮，一共有 {people} 个人信了煮\n你获得了 {point} 快乐',
                                f'总共有 {people} 个人因为你而信了煮\n你获得了 {point} 快乐',
                                f'煮不在糊祂多了 {people} 个信徒\n但你获取了 {point} 快乐'])
    await belief.send(dates() + events, at_sender=True)
    player_data[str(event.group_id)][str(event.user_id)]['is_belief'] = True
    with open(file, 'w', encoding='utf8') as f:
        json.dump(player_data, f, ensure_ascii=False, indent=4)


book = on_command("解读面经", priority=5)
@book.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    player_is_exists(event)
    if player_data[str(event.group_id)][str(event.user_id)]['job'] != 2:
        await sing.finish("你不是传教士，无法解读")
    if player_data[str(event.group_id)][str(event.user_id)]['is_jail']:
        if player_data[str(event.group_id)][str(event.user_id)]['jail'] == 0:
            player_data[str(event.group_id)][str(event.user_id)]['is_jail'] = False
        else:
            jail = player_data[str(event.group_id)][str(event.user_id)]['jail']
            await sing.finish(f"你在监狱里，还剩 {jail} 天释放")
    
    args = str(event.get_message()).strip()
    if args:
        state["type"] = args

@book.got("type", prompt=f"解读面经需要消耗快乐值，并以【1快乐:2金币】的比例换取金币\n你想要换取多少金币？")
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    player_is_exists(event)
    
    value = state["type"]
    value = int(value)
    happy = player_data[str(event.group_id)][str(event.user_id)]['happy']
    if happy < value:
        await book.finish(f'你只有 {happy} 快乐值，无法兑换')
    if value <= 0:
        await book.finish(f'太少了，无法兑换')
    player_data[str(event.group_id)][str(event.user_id)]['happy'] -= value
    value = value * 2
    player_data[str(event.group_id)][str(event.user_id)]['gold'] += value
    happy = player_data[str(event.group_id)][str(event.user_id)]['happy']
    gold = player_data[str(event.group_id)][str(event.user_id)]['gold']
    await book.send(f'兑换完毕！\n你现在有 {happy} 快乐、{gold} 金币')
    with open(file, 'w', encoding='utf8') as f:
        json.dump(player_data, f, ensure_ascii=False, indent=4)


potato = on_command("削土豆", priority=5)
@potato.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    player_is_exists(event)
    if player_data[str(event.group_id)][str(event.user_id)]['is_jail']:
        if player_data[str(event.group_id)][str(event.user_id)]['jail'] == 0:
            player_data[str(event.group_id)][str(event.user_id)]['is_jail'] = False
            await potato.finish("你已经出狱了！")
        else:
            pass
    else:
        await potato.finish("你不在监狱里！")
    
    rnd = random.Random()
    ptt = rnd.randint(1, 15)
    gold = ptt * 2
    player_data[str(event.group_id)][str(event.user_id)]['jail'] -= 1
    jail = player_data[str(event.group_id)][str(event.user_id)]['jail']
    if jail == 0:
        player_data[str(event.group_id)][str(event.user_id)]['is_jail'] = False
        events = f'你削了 {ptt} 个土豆，监狱决定给你 {gold} 金币作为奖赏，并减去了一天刑期\n你出狱了！'
    else:
        events = f'你削了 {ptt} 个土豆，监狱决定给你 {gold} 金币作为奖赏，并减去了一天刑期\n你还剩 {jail} 天出狱'
    await belief.send(dates() + events, at_sender=True)
    player_data[str(event.group_id)][str(event.user_id)]['gold'] += gold
    with open(file, 'w', encoding='utf8') as f:
        json.dump(player_data, f, ensure_ascii=False, indent=4)


#——————————————————————————————————————————————————————————————————————————————————————————#
### 家庭教师 ###
teach = on_command("教学", aliases={'讲课', '教书'}, priority=5)
@teach.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    player_is_exists(event)
    if player_data[str(event.group_id)][str(event.user_id)]['job'] != 3:
        await sing.finish("你不是家庭教师，无法自习")
    if player_data[str(event.group_id)][str(event.user_id)]['is_teach']:
        await sing.finish("今天已经教学过了！")

    rnd = random.Random()
    question = rnd.randint(1, 15)
    wisdom = player_data[str(event.group_id)][str(event.user_id)]['wisdom']
    gold = (wisdom + 1) * question
    gold = gold / 2
    gold = math.floor(gold)
    a = rnd.randint(1, 3)
    brain = a * question
    events = f'你教会了 {question} 道题\n你从中获取了 {brain} 智慧、{gold} 金币'
    await teach.send(dates() + events, at_sender=True)
    player_data[str(event.group_id)][str(event.user_id)]['is_teach'] = True
    player_data[str(event.group_id)][str(event.user_id)]['wisdom'] += brain
    player_data[str(event.group_id)][str(event.user_id)]['gold'] += gold
    player_data[str(event.group_id)][str(event.user_id)]['make_gold'] += gold
    with open(file, 'w', encoding='utf8') as f:
        json.dump(player_data, f, ensure_ascii=False, indent=4)


study = on_command("自习", priority=5)
@study.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    player_is_exists(event)
    if player_data[str(event.group_id)][str(event.user_id)]['job'] != 3:
        await sing.finish("你不是家庭教师，无法教学")
    if player_data[str(event.group_id)][str(event.user_id)]['is_study'] >= 5:
        await sing.finish("今天的自习上限已经到了！")
    
    rnd = random.Random()
    question = rnd.randint(1, 30)
    a = rnd.randint(1, 5)
    brain = a * question
    events = f'自习时，你刷了 {question} 道题\n你获取了 {brain} 智慧'
    await study.send(dates() + events, at_sender=True)
    player_data[str(event.group_id)][str(event.user_id)]['wisdom'] += brain
    player_data[str(event.group_id)][str(event.user_id)]['is_study'] += 1
    with open(file, 'w', encoding='utf8') as f:
        json.dump(player_data, f, ensure_ascii=False, indent=4)