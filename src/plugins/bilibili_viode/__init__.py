from nonebot import get_driver
from nonebot.plugin.manager import PluginLoader

from .config import Config
from .main import *

if isinstance(globals()["__loader__"], PluginLoader):
    global_config = get_driver().config
    config = Config(**global_config.dict())


__help_plugin_name__ = 'B站视频分享卡片'
__des__ = 'Bilibili视频分享卡片'
__author__ = 'ASTWY'
__level__ = '1'
__cmd__ = '''
发送Bilibili视频ID
'''.strip()
__example__ = '''
BV114514
'''.strip()
__note__ = '''
- N/A'''
__usage__ = f'''{__des__}
作者：{__author__}
权限等级：{__level__}
用法：{__cmd__}
举例：{__example__}
备注：{__note__}'''