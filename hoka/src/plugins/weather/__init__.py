from nonebot import on_command
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event


__usage__ = '''weather插件
[天气] -> 让hoka帮你查询天气'''
__help_plugin_name__ = '查询天气'
__priority__ = 6


weather = on_command("天气", rule=to_me(), priority=6)
@weather.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    if args:
        state["city"] = args

@weather.got("city", prompt="你想查询哪个城市的天气呢？")
async def handle_city(bot: Bot, event: Event, state: T_State):
    city = state["city"]
    city_weather = await get_weather(city)
    await weather.finish(city_weather)

async def get_weather(city: str):
    return f"{city}的天气我不知道呢"