from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from config.config import OWNER


__usage__ = '''auto-reply插件
[-] <文本>* -> 和hoka一起聊天吧！'''
__help_plugin_name__ = '自动回复'


reply = on_command("-", rule=to_me(), priority=10)
@reply.handle()
async def first_handle(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message()).strip()
    use_jb = False
    if "我是" in msg:
        ids = event.get_session_id()
        if ids.startswith("group"):
            _, group_id, user_id = event.get_session_id().split("_")
            if user_id in OWNER:
                use_jb = True
        else:
            user_id = ids
            if ids.startswith("group"):
                _, user_id = event.get_session_id().split("_")
                if user_id in OWNER:
                    use_jb = True
        if use_jb:
            await reply.finish("我超，爹！")
        else:
            await reply.finish("你寄吧谁啊，请再说一遍")
    elif "你是" in msg:
        await reply.finish('我是hoka-bot喔！我爹是王兄~\n请使用 [hoka help] 指令来获取hoka的命令列表！')
    elif "我" in msg:
        response = msg.replace('我','你').replace('吗','').replace('？','！')
    else:
        response = msg.replace('你','我').replace('吗','').replace('？','！')
    await reply.finish(response)