import re
import time
import random
from math import sqrt, factorial, log
from nonebot import on_command
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp import MessageSegment
from config.config import SUPERUSERS, ALL_GROUP
from config.path_config import IMAGE_PATH


__usage__ = '''calculator插件
原作者：【starvapour】
[计算帮助] -> 查看计算机功能'''
__help_plugin_name__ = '计算机'
__priority__ = 6


cd = 10
factorial_limit = 100
last_response = time.time() - cd
path = IMAGE_PATH + "/calculator"
#think_img = open(path + '/learn.png')
#think_img = random.choice(think_img)


calculator_help = on_command("计算帮助", priority=1)
@calculator_help.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    await calculator_help.finish(f'''计算机功能帮助：
[计算] <算式>：
    【命令响应冷却时间为：{cd}秒】
    【现不支持幂运算】
    【阶乘计算输入值不得超过{factorial_limit}】
    【示例：
        3+3j 为 虚数
        3e3 或 3e-3 或 3E3 为 科学计数法表示的数字
        abs(-3) 为 绝对值
        sqrt(3) 为 平方根
        // 为 整除
        % 为 求余数
        factorial(3) 为 阶乘
        log(3,3) 为 对数】''')


calculator = on_command("计算", priority=6)
@calculator.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    global last_response
    use_calculator = False
    ids = event.get_session_id()
    
    if ids.startswith("group"):
        _, group_id, user_id = event.get_session_id().split("_")
        if group_id in ALL_GROUP:
            use_calculator = True
    else:
        user_id = ids
        use_calculator = True
    if use_calculator:
        if time.time() - last_response >= cd or user_id in SUPERUSERS:
            msg = str(event.get_message()).strip().replace('\r\n','').replace('\n','').replace('（','(').replace('）',')').replace('，',',')
            require = "(\d| |\+|\-|\*|/|\(|\)|abs\(|sqrt\(|factorial\(|%|E|e|\.|log\(|\,|j)*"

            facts = re.findall("factorial\(\d*\)", msg)
            facts = list(map(lambda x: int(x[10:-1]), facts))
            large_fact = False
            for fact in facts:
                if fact > factorial_limit:
                    large_fact = True
                    break

            if msg != re.match(require, msg, flags=0).group() or "**" in msg:
                last_response = time.time()
                await calculator.finish("错误：输入算式中含有非法格式，请使用[计算帮助]查询规范。")
            elif large_fact:
                await calculator.finish("错误：输入算式中阶乘输入值过大，请使用[计算帮助]查询规范。")
            else:
                try:
                    result = round(eval(msg), 5)
                except ZeroDivisionError:
                    last_response = time.time()
                    await calculator.finish("错误：除数为零，怎么会有人把饼干分给0个人？")
                except:
                    last_response = time.time()
                    await calculator.finish("错误：输入算式并不是正确的算式")
                else:
                    last_response = time.time()
                    msg = "计算结果：" + str(result)
                    await bot.send(event=event, message=msg)