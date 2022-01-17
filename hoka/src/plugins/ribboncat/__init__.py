import random
from nonebot.plugin import on_command
from nonebot.adapters.cqhttp import Bot, Event, MessageSegment
from config.path_config import IMAGE_PATH


__usage__ = f'''ribboncat插件
[来点猫图] -> 随机抽取一张领结猫图
'''
__help_plugin_name__ = '随机领结猫'
__priority__ = 7


cat = on_command("来点猫图", priority=7)
@cat.handle()
async def cat_handle(bot: Bot, event: Event):
    path = IMAGE_PATH + "/ribboncat"
    img_list = open(path + '/resource.txt', "r", encoding="utf-8").read().replace("\n", "").split(".webp")
    gif = open(path + '/nibeipianle.gif')
    rnd = random.Random()
    rnd.seed()
    catnum = rnd.randint(0,3)
    if catnum == 0:
        gif = random.choice(gif) + ".gif"
        await bot.send(event=event, message=MessageSegment.image(gif), at_sender=True)
    elif catnum == 1:
        await cat.finish("你中了大奖，没抽到猫图！", at_sender=True)
    else:
        cat_img = random.choice(img_list) + ".webp"
        await bot.send(event=event, message=MessageSegment.image(cat_img), at_sender=True)