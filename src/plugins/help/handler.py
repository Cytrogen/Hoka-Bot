import nonebot.plugin

from nonebot.log import logger
from nonebot.rule import to_me
from nonebot.matcher import Matcher
from nonebot.params import CommandArg, Arg
from nonebot.plugin import on_command
from nonebot.adapters import Event, Bot
from nonebot.adapters.onebot.v11.message import Message, MessageSegment

from utils.rauthman import isInService


default_start = list(nonebot.get_driver().config.command_start)[0]


helper = on_command("help", 
                    priority=1, 
                    aliases={"帮助"}, 
                    rule=to_me())

                    
@helper.handle()
async def _(event: Event, matcher: Matcher, args: Message = CommandArg()):
    at = MessageSegment.at(event.get_user_id())
    if args:
        logger.warning(f"DETECTED ARGS{args}")
        matcher.set_arg("content", args)

    else:
        await matcher.finish(Message(at + 
        f'''欢迎使用Hoka-Bot！
        支持使用的前缀：{" ".join(list(nonebot.get_driver().config.command_start))}
        {default_start}help --> 获取本插件帮助
        {default_start}help list --> 展示已加载插件列表
        {default_start}help <插件名> --> 调取目标插件帮助信息
        
        发送 [功能] 以查询该群已开启的功能！'''))


@helper.got("content")
async def get_result(event: Event, content: Message = Arg()):
    at = MessageSegment.at(event.get_user_id())
    args = content.extract_plain_text().split()
    logger.warning(args)
    if str(args[0]).lower() == "list":
        plugin_set = nonebot.plugin.get_loaded_plugins()
        plugin_names = []
        for plugin in plugin_set:
            
            try:
                name = f'{plugin.name} | ' \
                    f'{plugin.module.__getattribute__("__help_plugin_name__")}'
            except:
                name = f'{plugin.name}'
            try:
                version = plugin.module.__getattribute__("__help_version__")
            except:
                version = ""
            plugin_names.append(f'{name} {version}')
        plugin_names.sort()
        newline_char = '\n'
        result = f'已加载插件：\n{newline_char.join(plugin_names)}'
    else:
        try:
            plugin = nonebot.plugin.get_plugin(args[0])
        except AttributeError:
            plugin = None
        try:
            matchers = plugin.matcher
            infos = {}
            index = 1
            for matcher in matchers:
                try:
                    name = matcher.__help_name__
                except AttributeError:
                    name = None
                try:
                    help_info = matcher.__help_info__
                except AttributeError:
                    help_info = matcher.__doc__
                if name and help_info:
                    infos[f'{index}. {name}'] = help_info
                    index += 1
            results = [plugin.module.__getattribute__("__usage__")]
            results.extend(
                [f'{key}: {value}' for key, value in infos.items()
                 if key and value]
            )
            result = '\n'.join(results)
        except:
            try:
                result = plugin.module.__doc__
            except AttributeError:
                result = f'{args[0]}插件不存在或未加载'
    await helper.finish(Message().append(at).append(
        MessageSegment.text(result)))


meow = on_command("hoka", 
                priority=2)
@meow.handle()
async def handle_send(bot: Bot):
    await meow.finish('喵')