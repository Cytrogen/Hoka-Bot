from nonebot.permission import SUPERUSER
import nonebot.plugin
from nonebot import on_command
from nonebot.log import logger
from nonebot.rule import to_me
from nonebot.typing import T_State
from nonebot.adapters import Bot, Event
from nonebot.adapters.cqhttp.message import Message, MessageSegment


helper = on_command("help", priority=1, rule=to_me(), aliases={"帮助"})
default_start = list(nonebot.get_driver().config.command_start)[0]
@helper.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    args = str(event.get_message()).strip()
    logger.debug(args)
    if args:
        state["content"] = args
    else:
        state["content"] = ""

@helper.got("content")
async def get_result(bot: Bot, event: Event, state: T_State):
    at = MessageSegment.at(event.get_user_id())
    if not state.get("content"):
        result = await get_help()
    elif str(state.get("content")).lower() == "list":
        plugin_set = nonebot.plugin.get_loaded_plugins()
        plugin_names = []
        for plugin in plugin_set:
            try:
                name = f'{plugin.module.__getattribute__("__help_plugin_name__")} | ' \
                    f'{plugin.name}'
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
            plugin = nonebot.plugin.get_plugin(state.get("content"))
        except AttributeError:
            plugin = None
        try:
            result = plugin.module.__getattribute__("__usage__")
        except:
            try:
                result = plugin.module.__doc__
            except AttributeError:
                result = f'{state.get("content")}插件不存在或未加载'
    await helper.finish(Message().append(at).append(MessageSegment.text(result)))


async def get_help():
    return f'''我是可爱的hoka酱喔~
指令前缀：{" ".join(list(nonebot.get_driver().config.command_start))}
[help]*  -> 获取本插件帮助
[update]* -> 查看hoka更新小日志
[-] <文本>* -> 自动回复
[私聊] <文本>* -> 私聊作者
[签到]* -> 获取金币以及抽签
[机器人帮助] -> 获取hoka指令的详解
[随机帮助] -> 获取随机指令的详解
[生成帮助] -> 获取所有生成指令的详解
[轮盘帮助] -> 获取俄罗斯轮盘指令的详解
[计算帮助] -> 获取计算机指令的详解
[轻量问答帮助] -> 获取问答指令的详解
[RSS帮助] -> 获取RSS订阅插件的详解
[职业帮助] -> 获取职业插件的详解
【*有该符号的代表该指令必须使用指令前缀】'''


# 帮助列表
russian = on_command("轮盘帮助", priority=2)
@russian.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    await russian.finish('''俄罗斯轮盘插件 指令：
[装弹] <子弹数> #金额# #@# -> 开始对决
[接受/拒绝] -> 接受对决/拒绝决斗
[开枪]
[结算] -> 当一方60秒未开枪，可以强行结束对决
[我的战绩]
[金币排行/胜场排行/败场排行/欧洲人排行/慈善家排行]''')


hoka_speak = on_command("机器人帮助", priority=2)
@hoka_speak.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    await hoka_speak.finish('''hoka机器人 帮助：
[help list]*  -> 展示已加载插件列表
[help] <插件名>*  -> 调取目标插件帮助信息
[状态] / 戳一戳 -> 调取服务器状态（仅 超级用户）
[say] <文本>* -> 可以解析CQ码的复读（仅 超级用户）
[echo] <文本>* -> 复读
[hoka]* -> 呼唤hoka
[天气]* -> 让hoka为你查询天气
[我爱你]*  -> 让hoka向你表白
[roll] <事件> <事件2> ... -> 让hoka为你挑选随机事件
[答案之书] <问题> -> 让hoka为你决定某件事
[早上/中午/下午/晚上好]  -> 给hoka打招呼
[缩写] <文本> -> 猜测缩写的原文字
[点歌] <歌名> -> 在QQ音乐中找到指定歌曲
[code] <语言> #-i# #输入# [代码] -> 在线写代码''')


random = on_command("随机帮助", priority=2)
@random.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    await random.finish('''随机 指令：
[抽牌] -> 抽取塔罗牌
[来点猫图] -> 抽取领结猫图
[来点二次元] -> 抽取二次元句子
[来点小学生] -> 抽取抖音小学生句子''')


create = on_command("生成帮助", priority=2)
@create.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    await create.finish('''生成 指令：
[cp] <攻> <受> -> 生成CP文
[体检] <名字> -> 生成体检图片
[鲁迅说] <文本>
[诺基亚/有内鬼] <文本>
[喜报] <文本>
[记仇] <文本>
[狂爱] <文本>
[低语] <文本>
[王境泽] <文本4>
[为所欲为] <文本9>
[馋身子] <文本3>
[切格瓦拉] <文本6>
[谁赞成谁饭对] <文本4>
[曾小贤/连连看] <文本4>
[压力大爷] <文本3>
[你好骚啊] <文本3>
[食屎啦你] <文本4>
[五年怎么过的] <文本4>
[我有个朋友] <@> <文本> -> 生成朋友说图片
[phlogo] <文本1> <文本2> -> 生成pornhub图标
[ytlogo] <文本1> <文本2> -> 生成youtube图标
[5000兆] <文本1> <文本2> -> 生成5000兆图片
[douyin] <文本> -> 生成抖音图标
[google] <文本> -> 生成谷歌图标
[虚假身份] #男/女# #生日# -> 指定男/女生成姓名，指定生日生成随机日期
[摸/亲/贴/顶/拍/撕/丢/爬/精神支柱/一直] <@/图片> -> 生成头像相关表情包''')


wordbank = on_command("轻量问答帮助", priority=2)
@wordbank.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    await wordbank.finish('''轻量问答插件 指令：
#模糊/正则/全局# [问] <触发句> [答] <答句> -> 设置词条(仅 超级用户、群主、管理员)
[删除 #全局# 词条] <触发句> -> 删除特定或全局词条（仅 超级用户、群主）
[删除全部词库] （仅 超级用户、群主）
[pd添加] <匹配率#> <sidxxx> [问]<图片> [答]<答句> -> 设置图片词条（同上）''')


rss = on_command('RSS帮助', aliases={'rss帮助'}, priority=2)
@rss.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    await rss.finish('''RSS订阅插件 指令：
[add] <订阅名> <RSS地址> -> 添加订阅
[delete] <订阅名> -> 删除订阅
[show_all/所有订阅] <关键词>
[show] <订阅名>
[change] <订阅名> <属性>=<值> -> 修改订阅
    【详细的参数列表见 [RSS参数帮助]】''')


rss_att = on_command('RSS参数帮助', aliases={'rss参数帮助'}, priority=2)
@rss_att.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    await rss_att.finish('''RSS参数列表：
订阅名 -name 字符串
订阅链接 -url 字符串
QQ号 -qq 整数/-1 （-1为空）
QQ群 -qun 整数/-1
更新频率 -time 整数/crontab字符串
代理 -proxy 1/0
翻译 -tl 1/0
仅标题 -ot 1/0
仅图片 -op 1/0
仅含有图片 -ohp 1/0
下载种子 -downopen 1/0
白名单关键词 -wkey 字符串/空
黑名单关键词 -bkey 字符串/空
种子上传到群 -upgroup 1/0
去重模式 -mode link/title/image/or/-1 （-1为禁用）
图片数量限制 -img_num 整数
正文待移除内容 -rm_list 字符串/-1
停止更新 -stop 1/0''')


work = on_command('职业帮助', priority=2)
@work.handle()
async def handle_first_receive(bot: Bot, event: Event, state: T_State):
    await rss.finish('''职业插件 指令：
[打工]*
[找工作]*
[辞职]*
[职业信息]
[我的职业]

[演唱会] -> 仅职业「爱豆」
[传教] -> 仅职业「传教士」
[解读面经] -> 仅职业「传教士」
[教学] -> 仅职业「家庭教师」
[自习] -> 仅职业「家庭教师」''')