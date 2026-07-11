---
audio: false
generated: true
image: false
lang: en
layout: post
title: WeChat Group Sync Bot Architecture
translated: false
type: note
---

Question: How to implement a "syncbot" that mirrors messages between 10 WeChat groups?

Answer:

The architecture is basically a **message relay system**:

```
WeChat Group A
      |
      v
  WeChat Bot Client
      |
      v
 Message Bus (Redis/Kafka)
      |
      v
  Sync Service
      |
      +----> Group B
      +----> Group C
      +----> ...
      +----> Group J
```

The hard part is **getting messages out of WeChat**. Official WeChat does not provide a normal group-message bot API for personal groups. You usually have these options:

---

## Option 1: WeChat personal account automation (most common)

Use libraries that control a logged-in WeChat account.

Examples:

* WeChaty
* itchat (older)
* iPad protocol bots (more powerful but risky)

Flow:

```
wechat account
    |
    | receive group message
    v
bot process
    |
    | normalize
    v
redis stream
    |
    | fan-out
    v
send to other groups
```

Minimal Python style:

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

## Option 2: Use a dedicated "bridge account"

Do not put your own WeChat account everywhere.

Create:

```
syncbot account

Group 1
  |
Group 2
  |
Group 3
  |
...
Group 10
```

The bot account joins all groups.

Advantages:

* easier management
* less spam from your personal account
* can add moderation

---

## Important design problems

### 1. Avoid infinite loops

Example:

```
Group A:
hello

syncbot copies:

Group B:
hello

syncbot sees hello again
copies back
```

Need message IDs.

Example:

```json
{
  "id": "uuid-123",
  "source": "group-a",
  "text": "hello"
}
```

Keep:

```
processed_messages = {
  uuid-123
}
```

---

### 2. Add prefix

Usually:

```
[Alice @ Group-A]

hello world
```

becomes:

```
[Group-A Alice]

hello world
```

---

### 3. Use async workers

10 groups is tiny.

A simple stack:

```
Python asyncio
      |
Redis Streams
      |
SQLite/Postgres
      |
Wechat adapter
```

No need Kafka.

---

## More scalable architecture

For 100+ groups:

```
                PostgreSQL
                    |
                Sync Engine
                    |
        +-----------+-----------+
        |                       |
   WeChat Adapter         WeChat Adapter
        |                       |
   Account #1              Account #2
```

Each WeChat account handles maybe 20-50 groups.

---

## Reality check

The biggest issue is not coding; it is **WeChat anti-bot detection**.

Tencent does not want uncontrolled bots:

* too many messages
* too many groups
* identical content forwarding

Typical mitigation:

* random delay (1-5 seconds)
* rate limiting
* human-like behavior
* dedicated accounts

For a private community of 10 groups, a single relay account + Redis queue is enough.

For a business/community product, a better approach is usually moving the community to platforms with official bot APIs:

* Telegram
* Discord
* Slack

because the same sync architecture becomes much cleaner.
