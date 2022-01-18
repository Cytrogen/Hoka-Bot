<div align="center">
    <h1>HOKA-BOT</h1>
</div>

<div align="center">
    <h3>一个基于 Nonebot2 和 Go-Cqhttp 的私用QQ群聊机器人</h3>
    <br>
    <img width="160" src="docs/HOKA现头像.jpg" alt="logo">
    </br>
    <div>任何BUG和反馈都可以写在ISSUE里</div>
    <br>
</div>

## 目录
  * [目录](#目录)
  * [使用](#使用)
    + [一步一步来！](#下载最新版本的go-cqhttp)
  * [功能](#功能)
  * [鸣谢](#鸣谢)

## 使用

配[这个文档](https://v2.nonebot.dev/)和[这个文档](https://docs.go-cqhttp.org/)食用更佳！

### 下载最新版本的[go-cqhttp](https://github.com/Mrs4s/go-cqhttp/releases)

存放至[这个文件夹](hokabot/)内，重命名为```go-cqhttp.exe```

同路径内应当有个.bat文件，如果没有，神说应当有.bat文件，里面应当是这样的：

```
%Created by go-cqhttp. DO NOT EDIT ME!%
start cmd /K go-cqhttp.exe
```

### 编辑[config.yaml](hokabot/config.yml)

需要编辑的地方有：

```
account: # 账号相关
  uin:  # QQ账号     <----这里！！！
  password: '' # 密码为空时使用扫码登录
  encrypt: false  # 是否开启密码加密
  status: 8      # 在线状态 请参考 https://docs.go-cqhttp.org/guide/config.html#在线状态
  relogin: # 重连设置
    delay: 3   # 首次重连延迟, 单位秒
    interval: 3   # 重连间隔
    max-times: 0  # 最大重连次数, 0为无限制

  # 是否使用服务器下发的新地址进行重连
  # 注意, 此设置可能导致在海外服务器上连接情况更差
  use-sso-address: false
```

```
# 连接服务列表
servers:
  # 添加方式，同一连接方式可添加多个，具体配置说明请查看文档
  #- http: # http 通信
  #- ws:   # 正向 Websocket
  #- ws-reverse: # 反向 Websocket
  #- pprof: #性能分析服务器
  # 反向WS设置
  - ws-reverse:
      # 反向WS Universal 地址
      # 注意 设置了此项地址后下面两项将会被忽略
      universal: ws://127.0.0.1:端口/cqhttp/ws   <----还有这里！！！把端口改了！！！
      # 反向WS API 地址
      api: ws://your_websocket_api.server
      # 反向WS Event 地址
      event: ws://your_websocket_event.server
      # 重连间隔 单位毫秒
      reconnect-interval: 3000
      middlewares:
        <<: *default # 引用默认中间件
```

### 编辑[环境设置](hoka/.env)

需要编辑的地方有：

```
HOST = 127.0.0.1
PORT = 端口     <----config.yaml上写了多少这里也写多少
DEBUG = false
OWNER = [""]   <----主人号
MAIN_GROUP = [""]    <----被我用来填了测试群的号
SUPERUSERS = ["", ""]    <----超级用户号，可以只填主人号一个
NICKNAME = ["hoka"]
COMMAND_START = ["hoka", ""]
COMMAND_SEP = ["*"]
```

```
LEETCODE_QQ_FRIENDS = [] <----定时发特定好友里扣
LEETCODE_QQ_GROUPS = []  <----定时发特定群聊里扣
LEETCODE_INFORM_TIME=[{"HOUR":,"MINUTE":},{"HOUR":,"MINUTE":}]  <----本地设备24小时制
```

- 需要注意的是，这里的```MAIN_GROUP```是[ELF_RSS2](hoka/src/plugins/ELF_RSS2/)插件会用到的
- 该用途为：每当hoka启动便会发送```MAIN_GROUP```一条提醒信息
- 因此建议填此处的```MAIN_GROUP```为屏蔽的小群，填下处的```MAIN_GROUP```为主要的测试群

### 编辑[config](hoka/config/config.py)

其实完全是多余项，只是本人比起.env更喜欢这个

以及懒得写权限

```
NICKNAME: str = "hoka"
BOT: str = ""
OWNER: str = ""
SUPERUSERS: List[Union[int, str]] = ["", ""]


# 主群&测试群
MAIN_GROUP: List[Union[int, str]] = ["", ""]
# 次群
SECOND_GROUP: List[Union[int, str]] = ["", ""]
# 剩下这两个都是啥东西啊我怎么建了这些
MAIN_SECOND_GROUP: List[Union[int, str]] = ["", "", ""]
ALL_GROUP: List[Union[int, str]] = ["", "", "", "", ""]
```

### 初始化nonebot

别忘了安装nonebot，此处仅展示用pip安装（其他方式请见nonebot文档）：

- ```pip install nb-cli```

进入**hoka文件夹**，开启任意命令提示符，输入```nb run```

此时bot.py将会被运行，nonebot被初始化，所有的插件被导入

- 如果有插件因为模块的原因**未能成功导入**，自行```pip install```该模块

当成功时，将会出现这个东西:

```
[INFO] uvicorn | Application startup complete.
```

### 运行cqhttp

快马加鞭进入**hokabot文件夹**，双击之前创建的go-cqhttp.bat

初次使用需要用到二维码扫描，扫完后便会登录

```
[INFO]: 已连接到反向WebSocket Universal服务器 ws://127.0.0.1:你的端口！/cqhttp/ws
```

出现上面这东西就代表连接成功，hoka可以使用噜！

## 功能

功能列表、简介均可使用 ```hoka help``` 和 ```hoka help list``` 来调取，并以其为标准

- [功能列表](docs/functions.md)

## 鸣谢

- [nonebot2](https://github.com/nonebot/nonebot2)，Python 异步机器人框架
- [go-cqhttp](https://github.com/Mrs4s/go-cqhttp)，cqhttp golang 原生实现
- [takker](https://github.com/FYWinds/takker)，娱乐性QQ机器人
- [sagiri-bot](https://github.com/SAGIRI-kawaii/sagiri-bot)，基于 Mirai 和 Graia 的 QQ机器人
- [luciabot](https://github.com/Box-s-ville/luciabot)，基于 Nonebot 的QQ机器人
- [绪山真寻bot](https://github.com/HibiKier/zhenxun_bot)，基于 Nonebot2 和 go-cqhttp 开发，以 postgresql 作为数据库的QQ群娱乐机器人
- [nonebot-plugin](https://github.com/fz6m/nonebot-plugin)，Nonebot 即开即用的插件
- [SetuBot](https://github.com/yuban10703/setu-nonebot2)，由 opq-osc/OPQ-SetuBot 的色图插件移植
- 以及更多的nonebot大佬！
