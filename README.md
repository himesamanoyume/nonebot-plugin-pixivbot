<!-- markdownlint-disable MD033 MD036 MD041 -->

<p align="center">
  <a href="https://v2.nonebot.dev/"><img src="https://v2.nonebot.dev/logo.png" width="200" height="200" alt="nonebot"></a>
</p>

<div align="center">

nonebot_plugin_pixivbot
=====

_✨ PixivBot ✨_

</div>

<p align="center">
  <a href="https://raw.githubusercontent.com/ssttkkl/nonebot-plugin-pixivbot/master/LICENSE">
    <img src="https://img.shields.io/github/license/ssttkkl/nonebot-plugin-pixivbot.svg" alt="license">
  </a>
  <a href="https://pypi.python.org/pypi/nonebot-plugin-pixivbot">
    <img src="https://img.shields.io/pypi/v/nonebot-plugin-pixivbot.svg" alt="pypi">
  </a>
  <img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="python">
</p>

NoneBot插件，支持发送随机Pixiv插画、画师更新推送、定时订阅推送……

## 触发语句

### 普通语句

所有数字参数均支持中文数字和罗马数字。

- **看看<类型>榜<范围>**：查看pixiv榜单（<类型>可省略，<范围>应为a-b或a）
    - 示例：看看榜、看看日榜、看看榜1-5、看看月榜一
- **来<数量>张图**：从推荐插画随机抽选一张插画（<数量>可省略，下同）
    - 示例：来张图、来五张图
- **来<数量>张<关键字>图**：搜索关键字，从搜索结果随机抽选一张插画
    - 示例：来张初音ミク图、来五张初音ミク图
    - 注：默认开启关键字翻译功能。Bot会在平时的数据爬取时记录各个Tag的中文翻译。在搜索时，若关键字的日文翻译存在，则使用日文翻译代替关键字进行搜索。
- **来<数量>张<用户>老师的图**：搜索用户，从插画列表中随机抽选一张插画
    - 示例：来张Rella老师的图、来五张Rella老师的图
- **看看图<插画ID>**：查看ID对应的插画
    - 示例：看看图114514
- **来<数量>张收藏**：从收藏中随机抽选一张插画（发送者需绑定Pixiv账号，或者在配置中指定默认Pixiv账号）
    - 示例：来张收藏、来五张收藏
- **还要**：重复上一次请求
- **不够色**：获取上一张插画的相关插画
- **收藏<插画ID>**：收藏id为<插画ID>的插画
- **取消收藏<插画ID>**：收藏id为<插画ID>的插画

### 命令语句

- **/pixivbot schedule \<type\> \<schedule\> [..args]**：为本群（本用户）订阅类型为<type>的定时推送功能，时间满足<schedule>时进行推送
    - \<type\>：可选值有ranking, random_bookmark, random_recommended_illust, random_illust, random_user_illust
    - \<schedule\>：格式为HH:mm（每日固定时间点推送）或HH:mm*x（间隔时间推送），或者使用cron表达式
    - [..args]：
        - \<type\>为ranking时，接受mode、range
            - 示例：/pixivbot schedule ranking 12:00 --mode day --range 1-10
        - \<type\>为random_bookmark时，接受user
            - 示例：/pixivbot schedule random_bookmark 01:00*x
            - 示例：/pixivbot schedule random_bookmark 01:00*x --user 114514
        - \<type\>为random_illust时，接受word（必需）
            - 示例：/pixivbot schedule random_illust "0 */2 * * * *" --word ロリ
            - 示例：/pixivbot schedule random_illust "0 */2 * * * *" --word "Hatsune Miku"
        - \<type\>为random_user_illust时，接受user（必需）
            - 示例：/pixivbot schedule random_user_illust 01:00*x --user 森倉円
        - \<type\>为random_recommend_illust时，不接受参数
- **/pixivbot schedule**：查看本群（本用户）的所有定时推送订阅
- **/pixivbot unschedule \<id\>**：取消本群（本用户）的指定的定时推送订阅
- **/pixivbot watch \<type\> [..args]**：为本群（本用户）订阅类型为<type>的更新推送功能
    - \<type\>：可选值有user_illusts, following_illusts
    - [..args]：
        - \<type\>为user_illusts时，接受user（必需）
            - 示例：/pixivbot watch user_illusts --user 森倉円
        - \<type\>为following_illusts时，接受user
            - 示例：/pixivbot watch following_illusts
            - 示例：/pixivbot watch following_illusts --user 114514
- **/pixivbot watch**：查看本群（本用户）的所有更新推送订阅
- **/pixivbot watch fetch \<id\>**：【调试用命令】立刻手动触发一次指定的更新推送订阅
- **/pixivbot unwatch \<id\> [..args]**：取消本群（本用户）的指定的更新推送订阅
- **/pixivbot bind \<pixiv_user_id\>**：绑定Pixiv账号（用于随机收藏功能）
- **/pixivbot unbind**：解绑Pixiv账号
- **/pixivbot invalidate_cache**：清除缓存（只有超级用户能够发送此命令）
- **/pixivbot**、**/pixivbot help**：查看帮助

## 环境配置

事前准备：登录pixiv账号并获取refresh_token。（参考：[@ZipFile Pixiv OAuth Flow](https://gist.github.com/ZipFile/c9ebedb224406f4f11845ab700124362)
、[eggplants/get-pixivpy-token](https://github.com/eggplants/get-pixivpy-token)）

1. 参考[安装 | NoneBot](https://v2.nonebot.dev/docs/start/installation)安装NoneBot；
2. 参考[创建项目 | NoneBot](https://v2.nonebot.dev/docs/tutorial/create-project)创建一个NoneBot实例；
3. 使用`nb plugin install nonebot-plugin-pixivbot`安装插件；
5. 在.env.prod中修改配置（参考下方）；

## 配置外部数据库（可选）

PixivBot需要使用数据库存放订阅以及缓存，默认使用SQLite。

### SQLite

若需要自定义SQLite数据库文件路径，请设置配置项：

- pixiv_sql_conn_url=`sqlite+aiosqlite:///<数据库文件路径>`

### PostgreSQL

若需要使用PostgreSQL，请设置配置项：

- pixiv_sql_conn_url=`postgresql+asyncpg://<用户名>:<密码>@<主机>:<端口>/<数据库名>`

并且执行`pip install asyncpg`安装asyncpg包

## 权限控制

插件接入了[nonebot-plugin-access-control](https://github.com/ssttkkl/nonebot-plugin-access-control)实现细粒度的权限控制：

```
nonebot_plugin_pixivbot
├── common
│   ├── illust  （看看图）
│   ├── ranking  （看看榜）
│   ├── more  （还要）
│   ├── random_bookmark  （来张收藏）
│   ├── random_illust  （来张xx图）
│   ├── random_recommended_illust  （来张图）
│   ├── random_related_illust  （不够色）
│   ├── random_user_illust  （来张xx老师的图）
│   ├── illust_bookmark_add  （收藏xx）
│   └── illust_bookmark_delete  （取消收藏xx）
├── illust_link  （P站链接嗅探）
├── schedule
│   ├── receive  （接收定时推送）
│   └── manage  （管理定时推送）
├── watch
│   ├── receive  （接收更新推送）
│   └── manage  （管理定时推送）
├── invalidate_cache  （清除缓存）
├── bind  （绑定P站账号）
├── help  （帮助文本）
└── r18  （显示R-18内容）
    └── g  （显示R-18G内容）
```

譬如，超级用户可以通过发送`/ac permission deny --srv nonebot_plugin_pixivbot.r18 --sbj all`全局拦截R-18。

又譬如，超级用户可以通过分别发送以下指令，使得只有超级用户、QQ私聊与QQ群聊的群管理能够调用`/pixivbot schedule`与`/pixivbot unschedule`命令。

```
/ac permission deny --srv nonebot_plugin_pixivbot.schedule.manage --sbj all
/ac permission allow --srv nonebot_plugin_pixivbot.schedule.manage --sbj qq:private
/ac permission allow --srv nonebot_plugin_pixivbot.schedule.manage --sbj qq:group_admin
/ac permission allow --srv nonebot_plugin_pixivbot.schedule.manage --sbj superuser
```

具体可以参考[nonebot-plugin-access-control](https://github.com/ssttkkl/nonebot-plugin-access-control)的文档进行权限控制。

## 常见问题

**遇到问题时请先尝试执行`pip install nonebot-plugin-pixivbot -U`更新到最新版本**。

Issue请尽可能带上详细的日志、配置文件与环境信息。功能请求请移步Discussion。

### 网络错误，请稍后再试（ No access_token Found!）

没登录成功，多半是网络问题。在国内请配置代理。

如果登录成功的话会在bot初始化后有这几句：

```
03-13 11:19:36 [SUCCESS] nonebot_plugin_pixivbot | refresh access token successfully. new token expires in 3600 seconds.
03-13 11:19:36 [DEBUG] nonebot_plugin_pixivbot | access_token: ***************
03-13 11:19:36 [DEBUG] nonebot_plugin_pixivbot | refresh_token: *****************
```

#### 如何配置代理

将`pixiv_proxy`配置项设为代理服务器地址（支持http、socks5协议）

```
pixiv_proxy=socks5://127.0.0.1:7890
```

### 发送合并转发消息惨遭风控

将`pixiv_send_forward_message`配置项设为`never`可禁用合并转发

### 内部错误：<class 'sqlalchemy.exc.OperationalError'>(sqlite3.OperationalError) near "ON": syntax error

多半是SQLite版本过低，不支持ON CONFLICT子句，如果是Linux系统请更新安装的SQLite版本

## 配置项一览

最小配置：

```
pixiv_refresh_token=  # 前面获取的REFRESH_TOKEN
```

除最小配置出现的配置项以外都是可选项，给出的是默认值，建议只将自己需要的项加入.env.prod文件

完整配置：

```
# 数据库配置
pixiv_sql_conn_url=sqlite+aiosqlite:///pixiv_bot.db  # SQL连接URL，仅支持SQLite与PostgreSQL（通过SQLAlchemy进行连接，必须使用异步的DBAPI）
pixiv_use_local_cache=True  # 是否启用本地缓存

# 连接配置
pixiv_refresh_token=  # 前面获取的REFRESH_TOKEN
pixiv_proxy=  # 代理URL，推荐使用socks5代理
pixiv_query_timeout=60  # 查询超时（单位：秒）
pixiv_loading_prompt_delayed_time=5  # 加载提示消息的延迟时间（“努力加载中”的消息会在请求发出多少秒后发出）（单位：秒）
pixiv_simultaneous_query=8  # 向Pixiv查询的并发数
pixiv_download_custom_domain=  # 使用反向代理下载插画的域名

# 查询设置
pixiv_query_to_me_only=False  # 只响应关于Bot的查询
pixiv_command_to_me_only=False  # 只响应关于Bot的命令

pixiv_max_item_per_query=10  # 每个查询最多请求的插画数量

pixiv_tag_translation_enabled=True  # 启用搜索关键字翻译功能（平时搜索时记录标签翻译，在查询时判断是否存在对应中日翻译）

pixiv_block_tags=[]  # 当插画含有指定tag时会被阻拦
pixiv_block_action=no_image  # 阻拦时的动作，可选值：no_image(不显示插画，回复插画信息), completely_block(只回复过滤提示), no_reply(无回复)

pixiv_send_illust_link=False  # 发图时是否带上链接（容易被tx盯上）
pixiv_send_illust_tags=False  # 发图时是否带上Tag
pixiv_send_illust_total_view  # 发图时是否带上浏览量
pixiv_send_illust_total_bookmarks  # 发图时是否带上收藏量
pixiv_send_illust_is_bookmarks  # 发图时是否带上当前插画的收藏状态
pixiv_send_illust_width_and_height  # 发图时是否带上插画尺寸

pixiv_exclude_ai_illusts=False  # 是否过滤AI绘图作品

pixiv_watch_interval=600  # 更新推送的查询间隔（单位：秒）

# 插画压缩
pixiv_compression_enabled=False  # 启用插画压缩
pixiv_compression_max_size=  # 插画压缩最大尺寸
pixiv_compression_quantity=  # 插画压缩品质（0到100）

# 缓存过期时间/删除时间（单位：秒）
pixiv_download_cache_expires_in=604800  # 默认值：7天
pixiv_illust_detail_cache_expires_in=604800
pixiv_user_detail_cache_expires_in=604800
pixiv_illust_ranking_cache_expires_in=21600  # 默认值：6小时
pixiv_search_illust_cache_expires_in=86400  # 默认值：1天
pixiv_search_illust_cache_delete_in=2592000  # 默认值：30天
pixiv_search_user_cache_expires_in=86400
pixiv_search_user_cache_delete_in=2592000
pixiv_user_illusts_cache_expires_in=86400
pixiv_user_illusts_cache_delete_in=2592000
pixiv_user_bookmarks_cache_expires_in=86400
pixiv_user_bookmarks_cache_delete_in=2592000
pixiv_related_illusts_cache_expires_in=86400
pixiv_other_cache_expires_in=21600

# QQ平台（主要是gocq）配置
pixiv_poke_action=random_recommended_illust  # 响应戳一戳动作，可选值：ranking, random_recommended_illust, random_bookmark, 什么都不填即忽略戳一戳动作
pixiv_send_forward_message=auto  # 发图时是否使用转发消息的形式，可选值：always(永远使用), auto(仅在多张图片时使用), never(永远不使用)

# 功能配置
pixiv_more_enabled=True  # 启用重复上一次请求（还要）功能
pixiv_query_expires_in=600  # 上一次请求的过期时间（单位：秒）

pixiv_illust_query_enabled=True  # 启用插画查询（看看图）功能

pixiv_ranking_query_enabled=True  # 启用榜单查询（看看榜）功能
pixiv_ranking_default_mode=day  # 默认查询的榜单，可选值：day, week, month, day_male, day_female, week_original, week_rookie, day_manga
pixiv_ranking_default_range=[1, 3]  # 默认查询的榜单范围
pixiv_ranking_fetch_item=150  # 每次从服务器获取的榜单项数（查询的榜单范围必须在这个数目内）
pixiv_ranking_max_item_per_query=5  # 每次榜单查询最多能查询多少项

pixiv_random_illust_query_enabled=True  # 启用关键字插画随机抽选（来张xx图）功能
pixiv_random_illust_method=bookmark_proportion  # 随机抽选方法，下同，可选值：bookmark_proportion(概率与收藏数成正比), view_proportion(概率与阅读量成正比), timedelta_proportion(概率与投稿时间和现在的时间差成正比), uniform(相等概率)
pixiv_random_illust_min_bookmark=0  # 过滤掉收藏数小于该值的插画，下同
pixiv_random_illust_min_view=0  # 过滤掉阅读量小于该值的插画，下同
pixiv_random_illust_max_page=20  # 每次从服务器获取的查询结果页数，下同
pixiv_random_illust_max_item=500  # 每次从服务器获取的查询结果项数，下同

pixiv_random_recommended_illust_query_enabled=True  # 启用推荐插画随机抽选（来张图）功能
pixiv_random_recommended_illust_method=uniform
pixiv_random_recommended_illust_min_bookmark=0
pixiv_random_recommended_illust_min_view=0
pixiv_random_recommended_illust_max_page=40
pixiv_random_recommended_illust_max_item=1000

pixiv_random_related_illust_query_enabled=True  # 启用关联插画随机抽选（不够色）功能
pixiv_random_related_illust_method=bookmark_proportion
pixiv_random_related_illust_min_bookmark=0
pixiv_random_related_illust_min_view=0
pixiv_random_related_illust_max_page=4
pixiv_random_related_illust_max_item=100

pixiv_random_user_illust_query_enabled=True  # 启用用户插画随机抽选（来张xx老师的图）功能
pixiv_random_user_illust_method=timedelta_proportion
pixiv_random_user_illust_min_bookmark=0
pixiv_random_user_illust_min_view=0
pixiv_random_user_illust_max_page=2147483647
pixiv_random_user_illust_max_item=2147483647

pixiv_random_bookmark_query_enabled=True  # 启用用户收藏随机抽选（来张收藏）功能
pixiv_random_bookmark_user_id=0  # 当QQ用户未绑定Pixiv账号时，从该Pixiv账号的收藏内抽选
pixiv_random_bookmark_method=uniform
pixiv_random_bookmark_min_bookmark=0
pixiv_random_bookmark_min_view=0
pixiv_random_bookmark_max_page=2147483647
pixiv_random_bookmark_max_item=2147483647

pixiv_illust_bookmark_manage_enabled=False  # 启用用户收藏或取消收藏插画（收藏/取消收藏）功能

```

## Special Thanks

- [Mikubill/pixivpy-async](https://github.com/Mikubill/pixivpy-async)

- [nonebot/nonebot2](https://github.com/nonebot/nonebot2)

## LICENSE

```
MIT License

Copyright (c) 2021 ssttkkl

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```
