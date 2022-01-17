import logging
from nonebot import get_driver, export
from nonebot.log import logger, LoguruHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .config import Config


__usage__ = f'''nonebot_plugin_apscheduler插件
原作者：【yanyongyu】
- 定时任务插件'''
__help_plugin_name__ = '定时任务'


driver = get_driver()
global_config = driver.config
plugin_config = Config(**global_config.dict())

scheduler = AsyncIOScheduler()
export().scheduler = scheduler


async def _start_scheduler():
    if not scheduler.running:
        scheduler.configure(plugin_config.apscheduler_config)
        scheduler.start()
        logger.opt(colors=True).info("<y>Scheduler Started</y>")


if plugin_config.apscheduler_autostart:
    driver.on_startup(_start_scheduler)

aps_logger = logging.getLogger("apscheduler")
aps_logger.setLevel(plugin_config.apscheduler_log_level)
aps_logger.handlers.clear()
aps_logger.addHandler(LoguruHandler())