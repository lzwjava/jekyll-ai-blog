---
audio: false
generated: true
image: false
lang: en
layout: post
title: Programmable Social Media Publishing Guide
translated: false
type: note
---

**Question: What social networks currently support programmable publishing via CLI/API for text, images, and videos?**

Answer:

If you want a **developer-first / CLI-first publishing workflow** (generate content → script → publish automatically), the landscape is roughly:

| Platform             | Text      | Image      | Video               | API/CLI friendliness | Notes                          |
| -------------------- | --------- | ---------- | ------------------- | -------------------- | ------------------------------ |
| X (formerly Twitter) | ✅         | ✅          | ✅                   | ⭐⭐⭐⭐⭐                | Best for bots, devs, AI agents |
| Mastodon             | ✅         | ✅          | ✅                   | ⭐⭐⭐⭐⭐                | Extremely API-friendly         |
| Bluesky              | ✅         | ✅          | ✅                   | ⭐⭐⭐⭐⭐                | AT Protocol, very programmable |
| Reddit               | ✅         | ✅          | limited             | ⭐⭐⭐⭐                 | Good for communities           |
| YouTube              | ❌         | thumbnails | ✅                   | ⭐⭐⭐⭐⭐                | Best video automation          |
| TikTok               | ❌         | ❌          | ✅                   | ⭐⭐⭐                  | API access more restricted     |
| Instagram            | ✅         | ✅          | ✅                   | ⭐⭐⭐                  | Requires business account      |
| LinkedIn             | ✅         | ✅          | ✅                   | ⭐⭐⭐                  | Good for professional content  |
| Hacker News          | text/link | ❌          | ❌                   | ⭐⭐⭐⭐                 | Simple API                     |
| GitHub               | markdown  | images     | videos via releases | ⭐⭐⭐⭐⭐                | Developer audience             |

---

## 1. Best programmable social networks

### 1. X API

Probably still the closest thing to a "social network terminal".

Example:

```bash
curl -X POST https://api.x.com/2/tweets \
-H "Authorization: Bearer $TOKEN" \
-d '{"text":"hello from my AI agent"}'
```

A daily AI agent could:

```
generate article
      |
      v
summarize
      |
      v
tweet thread
      |
      v
attach generated image
      |
      v
publish
```

This is why many AI agents integrate X.

---

## 2. Mastodon

Very Unix-like.

Create a bot:

```bash
curl \
  -X POST \
  https://mastodon.social/api/v1/statuses \
  -H "Authorization: Bearer $TOKEN" \
  -F "status=hello world"
```

Supports:

* text
* images
* videos
* polls
* scheduling

Great for open-source AI agents.

---

## 3. Bluesky / AT Protocol

Very interesting because it is designed as a programmable protocol.

Architecture:

```
Your Agent
    |
    |
AT Protocol
    |
    |
Bluesky Network
```

You can create:

* AI bloggers
* autonomous accounts
* research bots
* content agents

Example Python:

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

## 4. YouTube automation

For video:

```
AI generate video
        |
        |
ffmpeg
        |
        |
YouTube API
        |
        |
publish
```

Example:

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

This is probably the strongest programmable video platform.

---

## 5. Reddit

Good for communities.

Example:

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

Useful for:

* research sharing
* project launches
* discussions

---

## 6. Developer-first publishing stack

For an AI engineer, I would build something like:

```
                 ┌───────────┐
                 │ LLM Agent │
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

One command:

```bash
publish \
 --topic "CUDA Graph optimization" \
 --image cuda.png \
 --video demo.mp4
```

Outputs:

```
X thread
Bluesky post
Mastodon post
YouTube short
Blog article
GitHub README
```

---

## Current ranking for AI-agent creators

My ranking:

### Best overall

1. 🥇 X
2. 🥈 Bluesky
3. 🥉 Mastodon
4. YouTube
5. Reddit
6. LinkedIn
7. Instagram/TikTok

For someone building AI agents, the interesting future is probably:

```
LLM
 |
tool calling
 |
social APIs
 |
autonomous publishing agents
```

The missing piece today is not APIs; it is **agent identity + reputation + moderation**. The protocol layer (AT Protocol, ActivityPub) is probably where many future AI-native social systems will grow.

References:

* [X API Documentation](https://developer.x.com/en/docs?utm_source=chatgpt.com)
* [Mastodon API Documentation](https://docs.joinmastodon.org/api/?utm_source=chatgpt.com)
* [Bluesky AT Protocol Documentation](https://docs.bsky.app/?utm_source=chatgpt.com)
* [YouTube Data API Documentation](https://developers.google.com/youtube/v3?utm_source=chatgpt.com)
* [Reddit API Documentation](https://www.reddit.com/dev/api/?utm_source=chatgpt.com)
