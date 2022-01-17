import re
from nonebot import require
from nonebot.log import logger
from apscheduler.executors.pool import ProcessPoolExecutor, ThreadPoolExecutor
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from . import rss_class, rss_parsing, util


@util.time_out(time=300)
async def check_update(rss: rss_class.Rss):
    logger.info(f"{rss.name} 检查更新")
    await rss_parsing.start(rss)


async def delete_job(rss: rss_class.Rss):
    scheduler = require("nonebot_plugin_apscheduler").scheduler
    try:
        scheduler.remove_job(rss.name)
    except Exception as e:
        logger.debug(e)


async def add_job(rss: rss_class.Rss):
    await delete_job(rss)
    if len(rss.user_id) > 0 or len(rss.group_id) > 0:
        rss_trigger(rss)


def rss_trigger(rss: rss_class.Rss):
    if re.search(r"[_*/,-]", rss.time):
        my_trigger_cron(rss)
        return
    scheduler = require("nonebot_plugin_apscheduler").scheduler
    trigger = IntervalTrigger(minutes=int(rss.time), jitter=10)
    scheduler.add_job(
        func=check_update,
        trigger=trigger, 
        args=(rss,),
        id=rss.name,
        misfire_grace_time=30,
        max_instances=1,
        default=ThreadPoolExecutor(64),
        processpool=ProcessPoolExecutor(8),
        coalesce=True,
    )
    logger.info(f"定时任务 {rss.name} 添加成功")


def my_trigger_cron(rss: rss_class.Rss):
    tmp_list = rss.time.split("_")
    times_list = ["*/5", "*", "*", "*", "*"]
    for index, value in enumerate(tmp_list):
        if value:
            times_list[index] = value
    try:
        trigger = CronTrigger(
            minute=times_list[0],
            hour=times_list[1],
            day=times_list[2],
            month=times_list[3],
            day_of_week=times_list[4],
            timezone="Asia/Shanghai",
        )
    except Exception as e:
        logger.error(f"创建定时器错误！cron:{times_list} E：{e}")
        return
    scheduler = require("nonebot_plugin_apscheduler").scheduler

    scheduler.add_job(
        func=check_update,
        trigger=trigger,
        args=(rss,),
        id=rss.name,
        misfire_grace_time=30,
        max_instances=1,
        default=ThreadPoolExecutor(64),
        processpool=ProcessPoolExecutor(8),
        coalesce=True,
    )
    logger.info(f"定时任务 {rss.name} 添加成功")
