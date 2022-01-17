import random
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, MessageEvent
from util.data import gedeng
from config.config import MAIN_GROUP


__usage__ = '''gedeng插件
[来点咯噔文学] -> 抽取咯噔文学句子
【该插件仅在部分授权的群聊中使用】
【该插件的所有文本皆为从网络上复制粘贴，不代表作者的任何观点】
'''
__help_plugin_name__ = '咯噔文学'
__priority__ = 7


fans = on_command("来点咯噔文学", aliases={'咯噔文学'}, priority=7)
@fans.handle()
async def _(bot: Bot, event: MessageEvent, state: T_State):
    use_fans = False
    ids = event.get_session_id()
    if ids.startswith("group"):
        _, group_id, user_id = event.get_session_id().split("_")
        if group_id in MAIN_GROUP:
            use_fans = True
    else:
        user_id = ids
        use_fans = True
    
    if use_fans:
        await fans.finish(random.choice(gedeng), at_sender=True)