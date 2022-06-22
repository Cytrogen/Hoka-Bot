from nonebot import on_command, get_driver
from nonebot.rule import to_me
from nonebot.params import State, CommandArg
from nonebot.typing import T_State
from nonebot.adapters.onebot.v11 import Bot, Event, Message



__help_plugin_name__ = '联系管理员'
__des__ = '私信Bot管理员'
__author__ = 'Cytrogen'
__level__ = 'N/A'
__cmd__ = '''
hoka 私聊/contact <文本>
'''.strip()
__example__ = '''
hoka 私聊 管理员我好喜欢你！为了你，我要免费为你写代码！
'''.strip()
__note__ = '''
- 请不要轰炸我的私信'''
__usage__ = f'''{__des__}
作者：{__author__}
权限等级：{__level__}
用法：{__cmd__}
举例：{__example__}
备注：{__note__}'''


super_id = get_driver().config.superusers


private = on_command("contact", 
                    aliases={'私聊'}, 
                    rule=to_me(), 
                    priority=2)
@private.handle()
async def _(bot: Bot, event: Event, state: T_State = State(), city: Message = CommandArg()):
    msg = city.extract_plain_text()
    user = super_id
    message = '收到一条私聊信息：\n'
    at_end = f'\n--{event.user_id}'
    await bot.send_private_msg(user_id=int(user), message=message+msg+at_end)
    await private.finish('私聊已经发给我爹啦！')