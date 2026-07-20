---
audio: false
generated: true
image: false
lang: zh
layout: post
title: CLI上传到YouTube和微信
translated: true
type: note
---

**问题：能否使用 CLI 工具将视频上传到微信视频号或 YouTube？**

回答：

对于 **YouTube** 可以。对于 **微信视频号**，由于没有公开的上传 API，难度更大，但浏览器自动化可以做到。

## 1. YouTube：官方支持 CLI 的方式

YouTube 拥有成熟的 API：

* 上传视频
* 设置标题/描述/标签
* 设置缩略图
* 定时发布
* 管理播放列表

一个极简的 Python 上传程序：

```bash
pip install google-api-python-client google-auth-oauthlib
```

示例：

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

然后将其封装为：

```bash
yt-upload video.mp4 \
  --title "GPT-2 training on RTX4070" \
  --public
```

这基本上是内容农场和 AI 媒体流水线的工作方式。

---

## 2. 微信视频号：无官方公开 API

微信视频号有所不同。

腾讯提供的 API 主要面向：

* 微信公众号
* 小程序
* 企业微信

但并没有通用的“向个人视频号上传视频”的 API。

可行的方案：

### 方案 A：浏览器自动化（最实用）

使用：

* Playwright
* Selenium
* Puppeteer

示例架构：

```
video.mp4
    |
    v
ffmpeg 预处理
    |
    v
Playwright
    |
    v
wechat.com / 创作者平台
    |
    v
上传
    |
    v
发布
```

伪代码：

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)

    page = browser.new_page()

    page.goto(
        "https://channels.weixin.qq.com/platform"
    )

    # 先手动登录

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

问题：

* 二维码登录
* 反爬检测
* UI 变化
* 账号风险

---

### 方案 B：内部/私有 API

部分工具对微信 API 进行了逆向工程。

典型模式：

```
CLI
 |
 | HTTP
 |
微信私有端点
 |
视频号后端
```

但：

* 不稳定
* 账号封禁风险
* 违反腾讯条款

对于重要账号，建议避免使用。

---

## 3. 构建 AI 内容工厂

针对你的“token 工厂 / 超级智能体”想法，实际的技术栈如下：

```
                 LLM Agent
                    |
        +-----------+-----------+
        |                       |
   脚本智能体             元数据智能体
        |                       |
        v                       v
     ffmpeg             标题/标签生成器
        |
        v
    video.mp4
        |
 +------+------+
 |             |
YouTube    微信视频号
 API        Playwright
```

CLI 命令：

```bash
video-agent \
  --input blog.md \
  --voice elevenlabs \
  --model qwen \
  --publish youtube,wechat
```

流水线：

1. 用 LLM 生成脚本
2. 生成语音
3. 用幻灯片/截图创建视频
4. 添加字幕
5. 自动上传

---

## 4. 现有开源工具

For YouTube：

* [yt-dlp GitHub](https://github.com/yt-dlp/yt-dlp?utm_source=chatgpt.com) — 下载、元数据、自动化生态系统
* [google-api-python-client documentation](https://github.com/googleapis/google-api-python-client?utm_source=chatgpt.com) — 官方 Google API 客户端

For video generation：

* [FFmpeg official site](https://ffmpeg.org/?utm_source=chatgpt.com)

---

针对你的用例（AI 工程博客 + 实验），我建议 **优先构建 YouTube 版本**，因为其 API 干净整洁。然后仅通过 Playwright 添加微信视频号作为分发适配器。核心内容工厂不应依赖微信不稳定的 UI。
