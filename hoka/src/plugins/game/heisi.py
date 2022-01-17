import os
import random
from pydantic.env_settings import BaseSettings
import requests
import datetime
from pathlib import Path
from os.path import dirname
from nonebot import on_command, logger
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot,MessageSegment,GroupMessageEvent
from config.config import MAIN_SECOND_GROUP
from .util import *
try:
    import ujson as json
except ModuleNotFoundError:
    import json


heisi_group = MAIN_SECOND_GROUP
heisi_cd = 60
path=dirname(__file__)+"/resources"
cddir=dirname(__file__)+"/cd"
hs_player = {}


his = on_command("his",aliases={".黑丝",".丝袜"})
@his.handle()
async def _(bot:Bot,event:GroupMessageEvent,state:T_State):
    gid=str(event.group_id)
    if os.path.exists(path)==False:
        logger.info("创建资源路径")
        os.mkdir(path)
    if os.path.exists(path+"/heisi.txt")==False:
        where_heisi=requests.get("https://cdn.jsdelivr.net/gh/yzyyz1387/blogimages/nonebot/heisi.txt").text
        logger.info(f"从gayhub下载资源文件  {path}/heisi.txt")
        with open(path+"/heisi.txt","w",encoding="utf-8") as heisitxt:
            heisitxt.write(where_heisi)
            heisitxt.close()

    if gid in heisi_group:
        img_list=open(path+"/heisi.txt","r",encoding="utf-8").read().replace("\n","").split(".jpg")
        img = random.choice(img_list)+".jpg"
        cdtxt=cddir+"/"+gid+"cd.txt"
        if os.path.exists(cddir)==False:
            os.mkdir(cddir)
        if os.path.exists(cdtxt)==False:
            with open(cdtxt,"w") as cd:
                timenow = datetime.datetime.now()
                cd.write(str(timenow))
                cd.close()
                logger.info("初始化成功")
                await bot.send(
                    event=event,
                    message="初始化成功，当前群已开通此功能，请再发一次命令开始使用"
                )
        else:
            global player_data, hs_player
            player_is_exists(event)
            money = state['money'] = 1000
            user_money = player_data[str(event.group_id)][str(event.user_id)]['gold']
            if money > user_money:
                await his.finish('你现在没有钱，买不起黑丝啦！\n【首次游玩请发送 [签到] 来获取金币】', at_sender=True)

            user_name = event.sender.card if event.sender.nickname else event.sender.nickname
            hs_player[event.group_id] = {1: event.user_id,
                                        'user': user_name,
                                        'money': money}

            cdtime=open(cdtxt,"r").read()
            cdtime=datetime.datetime.strptime(cdtime,"%Y-%m-%d %H:%M:%S.%f")
            now=datetime.datetime.now()
            if int(str((now-cdtime).seconds))>int(heisi_cd):
                gold = hs_player[event.group_id]['money']
                hs_user_id = hs_player[event.group_id][1]

                hs_user_id = str(hs_user_id)
                group_id = event.group_id
                group_id = str(group_id)
                player_data[group_id][hs_user_id]['gold'] -= gold
                with open(cdtxt, "w") as cd:
                    timenow = datetime.datetime.now()
                    cd.write(str(timenow))
                    cd.close()
                own_gold = player_data[str(event.group_id)][str(event.user_id)]['gold']
                msg = f'你想要色色，于是hoka顺走了你的1000金币\n你还有 {own_gold} 金币'
                await bot.send(event=event, message=MessageSegment.image(img) + msg)
                hs_player[event.group_id] = {}
                with open(file, 'w', encoding='utf8') as f:
                    json.dump(player_data, f, ensure_ascii=False, indent=4)
            else:
                left=int(heisi_cd)-int(str((now-cdtime).seconds))
                await bot.send(event=event, message="技能CD中，剩%d秒"%left)
    else:
        logger.info(f"群  {event.group_id} 未开通此功能，发送提示信息 ")
        await bot.send(event=event, message="当前群未开通此功能")