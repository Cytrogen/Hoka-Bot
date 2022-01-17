import shlex
import traceback
from typing import Type
from nonebot import on_command
from nonebot.matcher import Matcher
from nonebot.typing import T_Handler, T_State
from nonebot.adapters.cqhttp import Bot, Event, MessageSegment
from nonebot.log import logger
from .data_source import make_meme, memes
from .download import DownloadError
from .functions import text_to_pic


__usage__ = '''memes插件
原作者：【MeetWq】
[鲁迅说] <文本>
[诺基亚] <文本>
[喜报] <文本>
[记仇] <文本>
[狂爱] <文本>
[低语] <文本>
[王境泽] <文本4>
[为所欲为] <文本9>
[馋身子] <文本3>
[切格瓦拉] <文本6>
[谁赞成谁饭对] <文本4>
[曾小贤] <文本4>
[压力大爷] <文本3>
[你好骚啊] <文本3>
[食屎啦你] <文本4>
[五年怎么过的] <文本4>'''
__help_plugin_name__ = 'memes制作'


help_cmd = on_command('表情包制作', priority=12)
@help_cmd.handle()
async def _(bot: Bot, event: Event, state: T_State):
    img = await text_to_pic(__usage__)
    if img:
        await help_cmd.finish(MessageSegment.image(img))


async def handle(matcher: Type[Matcher], event: Event, type: str):
    text = event.get_plaintext().strip()
    if not text:
        await matcher.finish()

    arg_num = memes[type].get('arg_num', 1)
    if arg_num == 1:
        texts = [text]
    else:
        try:
            texts = shlex.split(text)
        except:
            await matcher.finish(f'参数解析错误，若包含特殊符号请转义或加引号')

    if len(texts) < arg_num:
        await matcher.finish(f'该表情包需要输入{arg_num}段文字')
    elif len(texts) > arg_num:
        await matcher.finish(f'参数数量不符，需要输入{arg_num}段文字，若包含空格请加引号')

    try:
        msg = await make_meme(type, texts)
    except DownloadError:
        logger.warning(traceback.format_exc())
        await matcher.finish('资源下载出错，请稍后再试')
    except:
        logger.warning(traceback.format_exc())
        await matcher.finish('出错了，请稍后再试')

    if not msg:
        await matcher.finish('出错了，请稍后再试')
    if isinstance(msg, str):
        await matcher.finish(msg)
    else:
        await matcher.finish(MessageSegment.image(msg))


def create_matchers():
    def create_handler(style: str) -> T_Handler:
        async def handler(bot: Bot, event: Event, state: T_State):
            await handle(matcher, event, style)
        return handler

    for type, params in memes.items():
        matcher = on_command(
            type, aliases=params['aliases'], priority=13)
        matcher.append_handler(create_handler(type))


create_matchers()