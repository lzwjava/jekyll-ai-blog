---
audio: false
generated: true
image: false
lang: en
layout: post
title: CLI Upload to YouTube and WeChat
translated: false
type: note
---

**Question: Could we use a CLI tool to upload videos to WeChat Channels or YouTube?**

Answer:

Yes for **YouTube**. For **WeChat Channels (微信视频号)**, it is much harder because there is no public upload API, but browser automation can work.

## 1. YouTube: official CLI-friendly way

YouTube has a mature API:

* Upload video
* Set title/description/tags
* Set thumbnail
* Schedule publish
* Manage playlists

A minimal Python uploader:

```bash
pip install google-api-python-client google-auth-oauthlib
```

Example:

```python
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

flow = InstalledAppFlow.from_client_secrets_file(
    "client_secret.json",
    SCOPES
)

credentials = flow.run_local_server(port=8080)

youtube = build(
    "youtube",
    "v3",
    credentials=credentials
)

request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": "My AI Experiment",
            "description": "Training GPT model from scratch",
            "tags": ["AI", "LLM"]
        },
        "status": {
            "privacyStatus": "public"
        }
    },
    media_body=MediaFileUpload(
        "video.mp4",
        chunksize=-1,
        resumable=True
    )
)

response = request.execute()

print(response["id"])
```

Then wrap it:

```bash
yt-upload video.mp4 \
  --title "GPT-2 training on RTX4070" \
  --public
```

This is basically how content farms and AI media pipelines work.

---

## 2. WeChat Channels: no official public API

微信视频号 is different.

Tencent provides APIs for:

* WeChat Official Account (公众号)
* Mini Programs
* Enterprise WeChat

But not a general "upload video to personal Video Channel" API.

Possible approaches:

### Option A: Browser automation (most practical)

Use:

* Playwright
* Selenium
* Puppeteer

Example architecture:

```
video.mp4
    |
    v
ffmpeg preprocessing
    |
    v
Playwright
    |
    v
wechat.com / creator platform
    |
    v
upload
    |
    v
publish
```

Pseudo:

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto(
        "https://channels.weixin.qq.com/platform"
    )

    # login manually first

    page.set_input_files(
        "input[type=file]",
        "video.mp4"
    )

    page.fill(
        "#title",
        "My AI Agent Demo"
    )

    page.click(
        "text=发布"
    )
```

The problem:

* QR login
* anti-bot detection
* UI changes
* account risk

---

### Option B: Internal/private APIs

Some tools reverse engineer WeChat APIs.

Typical pattern:

```
CLI
 |
 | HTTP
 |
WeChat private endpoint
 |
Video Channel backend
```

But:

* unstable
* account ban risk
* violates Tencent terms

I would avoid for a serious account.

---

## 3. Building an AI content factory

For your "token factory / super-agent" idea, the practical stack:

```
                 LLM Agent
                    |
        +-----------+-----------+
        |                       |
   Script Agent             Metadata Agent
        |                       |
        v                       v
     ffmpeg              title/tag generator
        |
        v
    video.mp4
        |
 +------+------+
 |             |
YouTube     WeChat
 API        Playwright
```

CLI:

```bash
video-agent \
  --input blog.md \
  --voice elevenlabs \
  --model qwen \
  --publish youtube,wechat
```

Pipeline:

1. Generate script with LLM
2. Generate voice
3. Create video with slides/screenshots
4. Add subtitles
5. Upload automatically

---

## 4. Existing open-source tools

For YouTube:

* [yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp?utm_source=chatgpt.com) — downloading, metadata, automation ecosystem
* [google-api-python-client documentation](https://github.com/googleapis/google-api-python-client?utm_source=chatgpt.com) — official Google API client

For video generation:

* [FFmpeg official site](https://ffmpeg.org/?utm_source=chatgpt.com)

---

For your use case (AI engineering blog + experiments), I would build **YouTube-first** because the API is clean. Then add WeChat Channels through Playwright only as a distribution adapter. The core content factory should not depend on WeChat's unstable UI.
