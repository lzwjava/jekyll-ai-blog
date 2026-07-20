---
audio: false
generated: true
image: false
lang: zh
layout: post
title: YouTube数据API v3指南
translated: true
type: note
---

问题：如何使用YouTube Data API v3？

答案：

YouTube Data API v3 是用于通过编程方式与YouTube交互的官方REST API。你可以使用它来：

* 搜索视频/频道
* 获取视频元数据
* 上传视频
* 管理播放列表
* 读取评论
* 管理自己的频道

对于CLI自动化（你之前关于上传视频的问题），关键部分是 **OAuth2 + `videos.insert`**。

官方文档：
[YouTube Data API v3 文档](https://developers.google.com/youtube/v3?utm_source=chatgpt.com)

---

## 1. 创建Google Cloud项目

前往：

[Google Cloud Console](https://console.cloud.google.com/?utm_source=chatgpt.com)

创建项目：

```text
my-youtube-cli
```

启用：

```
APIs & Services
    ↓
Library
    ↓
YouTube Data API v3
    ↓
Enable
```

---

## 2. 创建OAuth凭据

对于上传视频，仅API密钥是不够的。

需要：

```
APIs & Services
    ↓
Credentials
    ↓
Create Credentials
    ↓
OAuth client ID
```

选择：

```
Desktop application
```

下载：

```
client_secret.json
```

示例：

```
youtube-cli/
 ├── client_secret.json
 └── upload.py
```

---

## 3. 安装Python SDK

```bash
pip install google-api-python-client google-auth-oauthlib
```

---

## 4. 上传视频示例

最小化上传脚本：

```python
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload"
]


flow = InstalledAppFlow.from_client_secrets_file(
    "client_secret.json",
    SCOPES
)

credentials = flow.run_local_server(
    port=8080
)


youtube = build(
    "youtube",
    "v3",
    credentials=credentials
)


request = youtube.videos().insert(
    part="snippet,status",
    body={
        "snippet": {
            "title": "我的AI生成视频",
            "description": "通过CLI上传",
            "tags": [
                "AI",
                "LLM"
            ],
            "categoryId": "28"
        },
        "status": {
            "privacyStatus": "private"
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

运行：

```bash
python upload.py
```

首次运行：

```
打开浏览器
↓
登录Google账号
↓
允许YouTube访问
↓
令牌缓存
```

之后，你的CLI就可以自动上传了。

---

## 5. 搜索视频

示例：

```python
youtube.search().list(
    part="snippet",
    q="GPT-5教程",
    maxResults=10,
    type="video"
).execute()
```

响应：

```json
{
 "items": [
   {
     "id": {
       "videoId": "abc123"
     },
     "snippet": {
       "title": "GPT-5教程"
     }
   }
 ]
}
```

---

## 6. 获取视频信息

```python
youtube.videos().list(
    part="snippet,statistics",
    id="VIDEO_ID"
).execute()
```

返回：

```json
{
 "statistics": {
   "viewCount": "12345",
   "likeCount": "500"
 }
}
```

---

## 7. 构建真正的AI视频流水线

对于AI内容工厂，架构可以是：

```
                LLM Agent
                    |
                    v
          生成脚本
                    |
                    v
        TTS / 虚拟形象 / 视频模型
                    |
                    v
              ffmpeg
                    |
                    v
             video.mp4
                    |
                    v
        YouTube Data API v3
                    |
                    v
              发布视频
```

CLI：

```bash
youtube upload \
    --file video.mp4 \
    --title "AI新闻 #001" \
    --privacy public
```

内部结构：

```
ww
 |
 +-- youtube.py
 |
 +-- oauth.py
 |
 +-- upload.py
```

---

## 8. 配额限制

YouTube API有配额：

默认值：

```
10,000 单位/天
```

重要成本：

| 操作           |       成本 |
| -------------- | ---------: |
| search.list    |  100 单位 |
| videos.list    |       1 单位 |
| upload video   | 1600 单位 |

因此：

```
10000 / 1600 ≈ 6 次上传/天
```

默认配额对于个人自动化来说足够，但视频工厂可能需要增加配额。

---

## 9. 多频道管理

每个频道需要：

```
Google账号
      |
OAuth授权
      |
refresh_token
      |
YouTube API
```

存储：

```
accounts/
 ├── channel_A.json
 ├── channel_B.json
 └── channel_C.json
```

然后：

```python
youtube = build(
    "youtube",
    "v3",
    credentials=channel_A_credentials
)
```

---

对于你的AI代理工作流，YouTube Data API实际上非常合适：代理可以生成内容、调用ffmpeg、上传、检查分析数据并迭代优化。主要瓶颈通常在于**内容生成 + 缩略图 + 分发**，而非API本身。