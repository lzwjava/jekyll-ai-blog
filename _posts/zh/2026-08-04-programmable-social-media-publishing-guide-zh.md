---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 可编程社交媒体发布指南
translated: true
type: note
---

**问题：目前有哪些社交网络支持通过 CLI/API 进行文本、图片和视频的可编程发布？**

答案：

如果你想要一个**开发者优先 / CLI 优先的发布工作流**（生成内容 → 脚本 → 自动发布），大致情况如下：

| 平台                 | 文本   | 图片   | 视频   | API/CLI 友好度 | 备注                             |
| -------------------- | ------ | ------ | ------ | -------------- | -------------------------------- |
| X（原 Twitter）       | ✅     | ✅     | ✅     | ⭐⭐⭐⭐⭐          | 最适合机器人、开发者、AI 代理     |
| Mastodon             | ✅     | ✅     | ✅     | ⭐⭐⭐⭐⭐          | 极其 API 友好                    |
| Bluesky              | ✅     | ✅     | ✅     | ⭐⭐⭐⭐⭐          | AT Protocol，可编程性极强         |
| Reddit               | ✅     | ✅     | 有限   | ⭐⭐⭐⭐           | 适合社区                         |
| YouTube              | ❌     | 缩略图 | ✅     | ⭐⭐⭐⭐⭐          | 最佳视频自动化                   |
| TikTok               | ❌     | ❌     | ✅     | ⭐⭐⭐            | API 访问受限较多                 |
| Instagram            | ✅     | ✅     | ✅     | ⭐⭐⭐            | 需要商业账号                     |
| LinkedIn             | ✅     | ✅     | ✅     | ⭐⭐⭐            | 适合专业内容                     |
| Hacker News          | 文本/链接 | ❌     | ❌     | ⭐⭐⭐⭐           | 简易 API                         |
| GitHub               | markdown | 图片   | 通过 releases 发布视频 | ⭐⭐⭐⭐⭐ | 面向开发者                       |

---

## 1. 最佳可编程社交网络

### 1. X API

很可能仍然是最接近“社交网络终端”的东西。

示例：

```bash
curl -X POST https://api.x.com/2/tweets \
-H "Authorization: Bearer $TOKEN" \
-d '{"text":"hello from my AI agent"}'
```

一个日常 AI 代理可以这样工作：

```
生成文章
      |
      v
总结
      |
      v
推文线程
      |
      v
附加生成的图片
      |
      v
发布
```

这就是为什么很多 AI 代理集成 X 的原因。

---

## 2. Mastodon

非常 Unix 风格。

创建一个机器人：

```bash
curl \
  -X POST \
  https://mastodon.social/api/v1/statuses \
  -H "Authorization: Bearer $TOKEN" \
  -F "status=hello world"
```

支持：

* 文本
* 图片
* 视频
* 投票
* 定时发布

非常适合开源 AI 代理。

---

## 3. Bluesky / AT Protocol

非常有趣，因为它被设计为一种可编程协议。

架构：

```
你的代理
    |
    |
AT Protocol
    |
    |
Bluesky 网络
```

你可以创建：

* AI 博主
* 自主账号
* 研究机器人
* 内容代理

Python 示例：

```python
from atproto import Client

client = Client()

client.login(
    "user",
    "password"
)

client.send_post(
    "hello from my AI agent"
)
```

---

## 4. YouTube 自动化

对于视频：

```
AI 生成视频
        |
        |
ffmpeg
        |
        |
YouTube API
        |
        |
发布
```

示例：

```python
youtube.videos().insert(
    part="snippet,status",
    body={
       "snippet":{
          "title":"AI generated video"
       }
    },
    media_body="video.mp4"
)
```

这可能是最强大的可编程视频平台。

---

## 5. Reddit

适合社区。

示例：

```python
import praw

reddit = praw.Reddit(
    client_id="...",
    client_secret="..."
)

subreddit = reddit.subreddit("MachineLearning")

subreddit.submit(
    "My AI experiment",
    selftext="details..."
)
```

适用于：

* 研究分享
* 项目发布
* 讨论

---

## 6. 开发者优先的发布栈

对于 AI 工程师，我会构建类似这样的东西：

```
                 ┌───────────┐
                 │ LLM 代理  │
                 └─────┬─────┘
                       |
        ┌──────────────┼──────────────┐
        |              |              |
        v              v              v

     X API        Bluesky API     Mastodon API

        |
        v

     YouTube API
        |
        v

     Blog/Jekyll/GitHub
```

一个命令：

```bash
publish \
 --topic "CUDA Graph optimization" \
 --image cuda.png \
 --video demo.mp4
```

输出：

```
X 线程
Bluesky 帖子
Mastodon 帖子
YouTube 短视频
博客文章
GitHub README
```

---

## 当前对 AI 代理创建者的排名

我的排名：

### 最佳整体

1. 🥇 X
2. 🥈 Bluesky
3. 🥉 Mastodon
4. YouTube
5. Reddit
6. LinkedIn
7. Instagram/TikTok

对于构建 AI 代理的人来说，有趣的未来可能是：

```
LLM
 |
工具调用
 |
社交 API
 |
自主发布代理
```

目前缺失的并不是 API，而是**代理身份 + 声誉 + 审核**。协议层（AT Protocol、ActivityPub）很可能是未来许多 AI 原生社交系统成长的地方。

参考资料：

* [X API 文档](https://developer.x.com/en/docs?utm_source=chatgpt.com)
* [Mastodon API 文档](https://docs.joinmastodon.org/api/?utm_source=chatgpt.com)
* [Bluesky AT Protocol 文档](https://docs.bsky.app/?utm_source=chatgpt.com)
* [YouTube Data API 文档](https://developers.google.com/youtube/v3?utm_source=chatgpt.com)
* [Reddit API 文档](https://www.reddit.com/dev/api/?utm_source=chatgpt.com)
