import httpx
from io import BytesIO
from nonebot import on_command
from nonebot.adapters.cqhttp import Bot, MessageEvent
from nonebot.adapters.cqhttp.event import GroupMessageEvent
from util.msg_util import image
from util.img_util import ImageUtil


__usage__ = '''friend_say插件
原作者：【FYWinds】
[我有个朋友] <@> <文本> -> 伪造一张朋友发来信息的图片'''
__help_plugin_name__ = '朋友说'
__priority__ = 9


friend = on_command("我有个朋友", aliases={"我有一个朋友", "我有朋友", "我有个朋友说"}, priority=9)
@friend.handle()
async def _(bot: Bot, event: MessageEvent):
    for num, seg in enumerate(event.message):
        if seg.type == "at":
            at = seg.data["qq"]
            text = (
                event.message[num + 1].data["text"].strip()
                if num + 1 <= len(event.message)
                else ""
            )
            break

    if not at or not text:
        return

    text = text[1:] if text.startswith("说") else text
    if len(text) > 31:
        await friend.finish("要说的内容太长了，建议削减", at_sender=True)
    else:
        url = "https://q1.qlogo.cn/g?b=qq&nk={}&s=100".format(at)

    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        avatar = r.content

    if isinstance(event, GroupMessageEvent):
        at_user = await bot.get_group_member_info(group_id=event.group_id, user_id=at)
        user_name = at_user["card"] if at_user["card"] else at_user["nickname"]
    else:
        user_name = (await bot.get_stranger_info(user_id=at))["nickname"]

    if avatar:
        ava = ImageUtil(100, 100, background=BytesIO(avatar))
    else:
        ava = ImageUtil(100, 100, color=(0, 0, 0))
    ava.circle()
    name = ImageUtil(300, 30, font_size=28)
    name.text((0, 0), user_name)
    img = ImageUtil(700, 150, font_size=25, color="white")
    img.paste(ava, (30, 25), alpha=True)
    img.paste(name, (150, 38))
    img.text((150, 85), text, (125, 125, 125))

    await friend.finish(image(c=img.toB64()))