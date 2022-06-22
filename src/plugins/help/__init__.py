import nonebot
from pathlib import Path

from .handler import *


default_start = list(nonebot.get_driver().config.command_start)[0]


# 存储所有的子插件
_sub_plugins = set()
# 加载所有的子插件
_sub_plugins |= nonebot.load_plugins(str((Path(__file__).parent / "plugins").resolve()))


__help_plugin_name__ = '帮助菜单'
__des__ = '帮助菜单'
__author__ = 'XZhouQD'
__level__ = '0'
__cmd__ = '''
hoka help
hoka help list
hoka help <插件名>
'''.strip()
__example__ = '''
hoka help help
'''.strip()
__note__ = '''
- N/A'''
__usage__ = f'''{__des__}
作者：{__author__}
权限等级：{__level__}
用法：{__cmd__}
举例：{__example__}
备注：{__note__}'''


nonebot.export.help = helper