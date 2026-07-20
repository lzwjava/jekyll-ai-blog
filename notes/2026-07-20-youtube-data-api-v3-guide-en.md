---
audio: false
generated: true
image: false
lang: en
layout: post
title: YouTube Data API v3 Guide
translated: false
type: note
---

Question: How to use YouTube Data API v3?

Answer:

YouTube Data API v3 is the official REST API for interacting with YouTube programmatically. You can use it to:

* Search videos/channels
* Get video metadata
* Upload videos
* Manage playlists
* Read comments
* Manage your own channel

For CLI automation (your previous question about uploading videos), the important part is **OAuth2 + `videos.insert`**.

Official docs:
[YouTube Data API v3 Documentation](https://developers.google.com/youtube/v3?utm_source=chatgpt.com)

---

## 1. Create Google Cloud project

Go to:

[Google Cloud Console](https://console.cloud.google.com/?utm_source=chatgpt.com)

Create project:

```text
my-youtube-cli
```

Enable:

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

## 2. Create OAuth credentials

For uploading videos, API key is not enough.

Need:

```
APIs & Services
    ↓
Credentials
    ↓
Create Credentials
    ↓
OAuth client ID
```

Choose:

```
Desktop application
```

Download:

```
client_secret.json
```

Example:

```
youtube-cli/
 ├── client_secret.json
 └── upload.py
```

---

## 3. Install Python SDK

```bash
pip install google-api-python-client google-auth-oauthlib
```

---

## 4. Upload video example

Minimal uploader:

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
            "title": "My AI generated video",
            "description": "Uploaded by CLI",
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

Run:

```bash
python upload.py
```

First time:

```
Open browser
↓
Login Google account
↓
Allow YouTube access
↓
Token cached
```

After that, your CLI can upload automatically.

---

## 5. Search videos

Example:

```python
youtube.search().list(
    part="snippet",
    q="GPT-5 tutorial",
    maxResults=10,
    type="video"
).execute()
```

Response:

```json
{
 "items": [
   {
     "id": {
       "videoId": "abc123"
     },
     "snippet": {
       "title": "GPT-5 tutorial"
     }
   }
 ]
}
```

---

## 6. Get video information

```python
youtube.videos().list(
    part="snippet,statistics",
    id="VIDEO_ID"
).execute()
```

Returns:

```json
{
 "statistics": {
   "viewCount": "12345",
   "likeCount": "500"
 }
}
```

---

## 7. Build a real AI video pipeline

For an AI content factory, architecture could be:

```
                LLM Agent
                    |
                    v
          Generate Script
                    |
                    v
        TTS / Avatar / Video Model
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
              Published Video
```

CLI:

```bash
youtube upload \
    --file video.mp4 \
    --title "AI News #001" \
    --privacy public
```

Internally:

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

## 8. Quota limits

YouTube API has quota:

Default:

```
10,000 units/day
```

Important costs:

| Operation    |       Cost |
| ------------ | ---------: |
| search.list  |  100 units |
| videos.list  |     1 unit |
| upload video | 1600 units |

So:

```
10000 / 1600 ≈ 6 uploads/day
```

Default quota is enough for personal automation, but a video factory may need quota increase.

---

## 9. For multiple channels

Each channel needs:

```
Google account
      |
OAuth authorization
      |
refresh_token
      |
YouTube API
```

Store:

```
accounts/
 ├── channel_A.json
 ├── channel_B.json
 └── channel_C.json
```

Then:

```python
youtube = build(
    "youtube",
    "v3",
    credentials=channel_A_credentials
)
```

---

For your AI-agent workflow, YouTube Data API is actually a good fit: an agent can generate content, call ffmpeg, upload, check analytics, and iterate. The main bottleneck is usually **content generation + thumbnail + distribution**, not the API itself.
