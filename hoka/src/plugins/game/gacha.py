import random
from nonebot import on_command, on_regex
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, GroupMessageEvent
from config.config import MAIN_GROUP, SECOND_GROUP
from .util import *
try:
    import ujson as json
except ModuleNotFoundError:
    import json


ck_player = {}


class NormalData:
    sixList = ['「高贵南龙王」椰子', '「重婚罪犯人」三十', '「高贵的东龙王」王兄', '「椰子黑站站长」小小',
                '「Project」Null', '「全村的希望」凯人']

    fiveList = ['「C语言终结者」椰子', '「黑历史挖掘者」椰子', '「美国历史见证者」黄大','「Java流浪者」黄大', '「三十岁继母」三十',
                '「物法双修魔法师女巫」三十', '「世界机构他爹」王兄', '「站街达人」Hoka-Bot',
                '「猛1」黄大', '「鲑鱼叉烧饭」三十', '「群主做RBQ」王兄', '「本群指定麦片哥」小小', '「万恶之源」APUSH', '「南极贱畜杀手」Null',
                '「MotherNotFound」企鹅', '「本群指定职业」码农', '「肖战邪神」王兄', '「戒赌带师」椰子', '「骗钱恶魔」王兄', '「变态XP者」三十',
                '「唯心主义时间控制者」Null', '「正太爱好者」黄大', '「Kami性恋」杨人', '「龙一内裤」凯人',
                '「不治的病魔」欧姆雷综合症', '「地下室霸王」龙一', '「蓝锁追求者」凯人', '「24小时发情王」凯人', '「高贵的学生会长」凯人',
                '「几何大师」Kami', '「毛茸茸国王」毛凯', '「毛毛果酱」毛雪', '「欧姆雷病人」凯人', '「野兽前辈」田所浩二', '「我的膝盖」Yu',
                '「初始的勇者」小不君', '「终焉的魔王」饿龙', '「羊肉灌汤包好次」王兄', '「自评代码」黄大']

    fourList = ['「抽不到XP」椰子', '「虎鲸」椰子', '「高数带师」椰子', '「物理特攻」黄大', '「兰陵王」黄大', '「Replit」黄大', '「女儿控」三十',
                '「Homo」王兄', '「海豹」三十', '「只想玩游戏」三十', '「被迫害者」王兄', '「美术生」王兄', '「倒垃圾狂魔」三十', '「花瓶收藏者」王兄',
                '「黄油搬运家」椰子', '「福瑞控」王兄', '「南极贱畜」TX', '「XP」狼人杀', '「过时版本」荒野乱斗', '「丢锅侠」Hoka-Bot',
                '「资本家」Hoka-Bot', '「去鼠」四叠半', '「绿帽菠菜」王兄', '「纯爱变态」凯人', '「性转」杨人', '「蜂蜜和盐」欧姆雷饼',
                '「牛油果」杨人', '「SAT老公」凯人', '「锁性恋」凯人', '「锅性恋」凯人', '「修厕所的」凯人', '「永恒微笑」Ginkgo Man',
                '「猫咪」Kami', '「下水道猫咪」三十', '「魅力UP」椰子', '「首」田所浩二', '「冲国人」凯人', '「口区」毛凯', '「天空下起了」毛雪',
                '「Go」Cqhttp', '「考研」Mirai', '「同性交友」GitHub', '「2BOM」东京放课后', '「勇者」小不君', '「魔王」饿龙', '「苹果」夜璃',
                '「老大哥」鬼鬼', '「韩娱」小小', '「小学漫画」TTH', '「小学游戏」GH', '「泰迪」Lucky', '「白毛控」王兄']

    threeList = ['Hoka-Bot', '椰子', '黄大', '三十', '王兄', '小小', 'Null', 'Java', 'Python', 'C语言', '欧姆雷蛋', '夜璃', '鬼鬼', '起司',
                'SkullGirls', '龙脉R', '四叠半', '东京放课后', 'LAH', 'Yu', 'C++', '小不君', 'APUSH', '企鹅', '剧本杀', '狼人杀', 'PowerShell',
                'NodeJs', 'LeetCode', 'MHY', '原神', '凯人', '杨人', '雪人', '龙一', '毛凯', '毛雪', 'Ginkgo Man', 'Kami', '欧姆雷饼',
                '欧姆雷综合症', '田所浩二', 'C#', 'Nonebot', 'Mirai', 'Graia', 'Cqhttp', 'JavaScript', 'GitHub', 'Kotlin', '饿龙', '明日方舟',
                '荒野乱斗', '码农', 'TTH', 'GH', 'Lucky']

    onelist = ['弱智虾虾']

    #圣诞节UP
    #fiveListUp = ['「限定」速开活动椰子', '「自评代码」黄大', '「限定」肯德基小小']
    #sixListUp = ['「限定」圣诞节恶魔', '「限定」放假打游戏三十']

    #新年UP
    #fiveListUp = ['「限定」压岁钱恶魔', '「限定」头脑鞭炮黄大', '「意面教传道」三十']
    #sixListUp = ['「限定」新年没有活动椰子', '「限定」新年送虾Hoka']

    fiveListUp = ['「本群指定男性」椰子', '「退休的黑历史收藏者」三十', '「猛男市场需求者」王兄']
    sixListUp = ['「北海龙王」黄大', '「世界机构」Hoka-Bot']


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


one = on_command('抽卡', aliases={'单抽'}, rule=to_me(), priority=5)
@one.handle()
async def arkRandom(bot: Bot, event: GroupMessageEvent, state: T_State):
    use_gacha = False
    ids = event.get_session_id()
    _, group_id, user_id = event.get_session_id().split("_")
    if group_id in MAIN_GROUP or group_id in SECOND_GROUP:
        use_gacha = True
    
    if use_gacha:
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
    else:
        await one.finish("该功能未在该群开通！")


ten = on_command('十连', rule=to_me(), priority=5)
@ten.handle()
async def arkRandomTen(bot: Bot, event: GroupMessageEvent, state: T_State):
    use_gacha = False
    ids = event.get_session_id()
    _, group_id, user_id = event.get_session_id().split("_")
    if group_id in MAIN_GROUP or group_id in SECOND_GROUP:
        use_gacha = True

    if use_gacha:
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
    else:
        await ten.finish("该功能未在该群开通！")


possibility = on_command('卡池', rule=to_me(), priority=5)
@possibility.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
    args = str(event.get_message()).strip()
    if args: 
        state["list"] = args

@possibility.got("list", prompt="想要查看几星的列表？")
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
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
    else:
        await possibility.finish('没有该稀有度，或者用汉字取代阿拉伯数字')


sell = on_regex('售卖(.*?)[个](.*?)星', priority=5)
@sell.handle()
async def _(bot: Bot, event: GroupMessageEvent, state: T_State):
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
            cost = 50
            a = '三'
        elif info[1] == 4:
            num = 'num4'
            cost = 100
            a = '四'
        elif info[1] == 5:
            num = 'num5'
            cost = 500
            a = '五'
        star = player_data[str(event.group_id)][str(event.user_id)][f'{num}']
        if amount > star:
            await sell.finish('售卖的数量大于你拥有的数量')
        cost = amount * cost
        player_data[str(event.group_id)][str(event.user_id)][f'{num}'] -= amount
        player_data[str(event.group_id)][str(event.user_id)]['gold'] += cost
        number = player_data[str(event.group_id)][str(event.user_id)][f'{num}']
        gold = player_data[str(event.group_id)][str(event.user_id)]['gold']
        with open(file, 'w', encoding='utf8') as f:
            json.dump(player_data, f, ensure_ascii=False, indent=4)
        await sell.finish(dates() + f'你售卖了 {amount} 个{a}星，获取了 {cost} 金币\n\n你现在拥有 {number} 个{a}星、{gold} 金币', at_sender=True)