from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters.cqhttp import Bot, PrivateMessageEvent, Event
from config.config import OWNER


__usage__ = '''contact插件
[contact] <文本>* -> 给作者发送私聊
【私聊可以是：反馈、建议、BUG、塞树洞等】'''
__help_plugin_name__ = '私聊作者'
__priority__ = 2


private = on_command("contact", aliases={'私聊'}, rule=to_me(), priority=2)
@private.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    msg = str(event.get_message()).strip()
    user = OWNER
    message = '收到一条私聊信息：\n'
    at_end = f'\n--{event.user_id}'
    await bot.send_private_msg(user_id=int(user), message=message+msg+at_end)
    await private.finish('私聊已经发给我爹啦！')