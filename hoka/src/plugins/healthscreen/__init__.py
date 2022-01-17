import io
import datetime
from PIL import Image, ImageDraw, ImageFont
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent
from util.msg_util import image
from config.config import MAIN_GROUP, SECOND_GROUP
from config.path_config import FONT_PATH, IMAGE_PATH


__usage__ = '''healthscreen插件可以生成每日体检用图片
[体检] <名字> -> 生成体检用图片
【该插件仅在部分授权的群聊中使用】
【该插件仅供PIL学习和娱乐用途使用】'''
__help_plugin_name__ = '每日体检'
__priority__ = 9


healthscreen = on_command("体检", aliases={"hs", "healthscreen"}, priority=9)
@healthscreen.handle()
async def handle(bot: Bot, event: MessageEvent, state: T_State):
    use_hs = False
    ids = event.get_session_id()
    if ids.startswith("group"):
        _, group_id, user_id = event.get_session_id().split("_")
        if group_id in MAIN_GROUP or group_id in SECOND_GROUP:
            use_hs = True
    else:
        user_id = ids
        use_hs = True
    
    if use_hs:
        args = event.get_plaintext()
        if args:
            state["content"] = args if args else "懒了，不想给你体检"


@healthscreen.got("content", prompt="你的名字是？")
async def handle_event(bot: Bot, event: MessageEvent, state: T_State):
    content = state["content"].strip()
    if content.startswith(",") or content.startswith("，"):
        content = content[1:]
    if len(content) > 20:
        await healthscreen.finish("你的名字就长的离谱", at_sender=True)
    else:
        img = image(c=process_pic(content))
        await healthscreen.send(img)


def process_pic(content) -> bytes:
    name = str(content)
    name = name.split()
    for i in range(len(name)):
        name[i] = name[i].capitalize()
    name = ' '.join(name)
    date = datetime.datetime.now().strftime('%A, %B %#d, %Y %#I:%M %p')

    hsimg = Image.open(IMAGE_PATH + "other/hs.jpg")
    hsimg_size = (1102,702)

    font_path = FONT_PATH + "/arialbd.ttf"
    namefont = ImageFont.truetype(font_path, size=30)
    datefont = ImageFont.truetype(font_path, size=50)

    text_width = datefont.getsize(date)
    text_height = 418.5
    text_coordinate = int((hsimg_size[0]-text_width[0])/2), int(text_height)

    draw = ImageDraw.Draw(hsimg)
    draw.text(xy=(145,35), text=name, fill="white", font=namefont)
    draw.text(text_coordinate, text=date, fill=(88,162,87), font=datefont)
    
    temp: io.BytesIO = io.BytesIO()
    hsimg.save(temp, format="PNG")
    result: bytes = temp.getvalue()
    return result