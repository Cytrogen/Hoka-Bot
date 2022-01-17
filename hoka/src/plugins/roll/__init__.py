import random
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent, GroupMessageEvent
from util.utils import get_message_text
from config.config import NICKNAME


__usage__ = """roll插件
原作者：【HibiKier】
[roll] <随机事件>
""".strip()
__help_plugin_name__ = '扔骰子'


roll = on_command("roll", priority=5, block=True)
@roll.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    msg = get_message_text(event.json()).split()
    if not msg:
        await roll.finish(f"roll: {random.randint(0, 100)}", at_sender=True)
    user_name = event.sender.card if event.sender.card else event.sender.nickname
    x = random.choice(msg)
    start = random.choice([
                "转动命运的齿轮，拨开眼前迷雾……",
                f"启动吧，命运的水晶球，为{user_name}指引方向！",
                "嗯哼，在此刻转动吧！命运！",
                f"在此祈愿，请为{user_name}降下指引……"])
    end = random.choice([
                f"\n让{NICKNAME}看看是什么结果！答案是：「{x}」",
                f"\n根据命运的指引，接下来{user_name} 「{x}」 会比较好",
                f"\n祈愿被回应了！是 「{x}」！",
                f"\n结束了，{user_name}，命运之轮停在了 「{x}」！"])
    await roll.finish(start + end)