import nonebot
from pathlib import Path
from .handler import helper


__usage__ = f'''nonebot-plugin-help插件
原作者：【XZhouQD】
支持使用的前缀：{" ".join(list(nonebot.get_driver().config.command_start))}
[help]* -> 获取本插件帮助
[help list]* -> 展示已加载插件列表
[help <plugin_name>]* -> 调取目标插件帮助信息
'''
__help_plugin_name__ = "插件帮助"
__priority__ = 1


default_start = list(nonebot.get_driver().config.command_start)[0]

# store all subplugins
_sub_plugins = set()
# load sub plugins
_sub_plugins |= nonebot.load_plugins(
    str((Path(__file__).parent / "plugins").resolve()))

nonebot.export.help = helper