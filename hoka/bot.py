import nonebot
from nonebot.adapters.cqhttp import Bot as CQHTTPBot
from pydantic import BaseConfig

#初始化nonebot
nonebot.init()
app = nonebot.get_asgi()

#连接驱动
driver = nonebot.get_driver()
driver.register_adapter("cqhttp", CQHTTPBot)
config = driver.config

#加载插件(除此处其他配置不建议更改)
nonebot.load_plugins('src/plugins')
nonebot.load_builtin_plugins()

#启动bot
if __name__ == "__main__":
    nonebot.logger.warning("Always use `nb run` to start the bot instead of manually running!")
    nonebot.run(app="__mp_main__:app")
