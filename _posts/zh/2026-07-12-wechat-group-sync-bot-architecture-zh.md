---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 微信群同步机器人架构
translated: true
type: note
---

问题：如何实现一个“syncbot”，在10个微信群之间镜像消息？

答案：

其架构本质上是一个**消息中继系统**：

```
微信群 A
      |
      v
  微信机器人客户端
      |
      v
 消息总线 (Redis/Kafka)
      |
      v
  同步服务
      |
      +----> 群 B
      +----> 群 C
      +----> ...
      +----> 群 J
```

难点在于**从微信中获取消息**。官方微信并未为个人群提供正常的群消息机器人 API。通常有以下几种选择：

---

## 方案一：微信个人账号自动化（最常见）

使用能控制已登录微信账号的库。

例如：

* WeChaty
* itchat（较旧）
* iPad 协议机器人（更强大但有风险）

流程：

```
微信账号
    |
    | 接收群消息
    v
机器人处理
    |
    | 标准化
    v
Redis 流
    |
    | 扇出
    v
发送到其他群
```

简化的 Python 风格：

```python
from redis import Redis

redis = Redis()

def on_message(msg):
    if msg.room:
        event = {
            "room": msg.room,
            "sender": msg.sender,
            "text": msg.text
        }

        redis.xadd(
            "wechat_messages",
            event
        )


def sync_worker():
    while True:
        messages = redis.xread(
            {"wechat_messages": "$"}
        )

        for msg in messages:
            for room in target_rooms:
                wechat.send(room, msg["text"])
```

---

## 方案二：使用专用的“桥接账号”

不要将自己的微信账号到处使用。

创建：

```
同步机器人账号

群 1
  |
群 2
  |
群 3
  |
...
群 10
```

机器人账号加入所有群。

优点：

* 更易管理
* 个人账号更少收到垃圾信息
* 可添加审核功能

---

## 重要的设计问题

### 1. 避免无限循环

示例：

```
群 A:
你好

同步机器人复制到：

群 B:
你好

同步机器人再次看到“你好”
又复制回去
```

需要消息 ID。

示例：

```json
{
  "id": "uuid-123",
  "source": "group-a",
  "text": "你好"
}
```

维护：

```
processed_messages = {
  uuid-123
}
```

---

### 2. 添加前缀

通常：

```
[Alice @ 群-A]

你好世界
```

变成：

```
[群-A Alice]

你好世界
```

---

### 3. 使用异步工作器

10 个群规模很小。

一个简单的技术栈：

```
Python asyncio
      |
Redis Streams
      |
SQLite/Postgres
      |
微信适配器
```

不需要 Kafka。

---

## 更具可扩展性的架构

对于 100+ 个群：

```
                PostgreSQL
                    |
                同步引擎
                    |
        +-----------+-----------+
        |                       |
   微信适配器              微信适配器
        |                       |
   账号 #1                 账号 #2
```

每个微信账号可以处理大约 20-50 个群。

---

## 现实情况

最大的问题不是编码，而是**微信的反机器人检测**。

腾讯不希望不受控制的机器人：

* 消息过多
* 群过多
* 转发相同的内容

常见的缓解措施：

* 随机延迟（1-5 秒）
* 速率限制
* 类似人类的行为
* 专用账号

对于 10 个群的私人社区，单个中继账号 + Redis 队列就足够了。

对于企业/社区产品，更好的做法通常是将社区迁移到具有官方机器人 API 的平台：

* Telegram
* Discord
* Slack

因为相同的同步架构在这些平台上会变得更加简洁。
