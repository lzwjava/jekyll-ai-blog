---
audio: false
generated: true
image: false
lang: en
layout: post
title: YouTube upload privacy update
translated: false
type: note
---

Done. Here's what I committed and pushed (2 commits on `main`):

**Commit 1** — `7bd9257`: Added `ww gen-video set-privacy`
- New command: `ww gen-video set-privacy <video_id> <public|unlisted|private>`
- Uses `youtube` scope, token cached at `~/.google/youtube_update_token.json`
- Fetches current video status, updates only the privacy field

**Commit 2** — `5a3e258`: Auto-public after upload
- Default privacy changed from `private` → `public`
- After upload succeeds, explicitly calls the update API to ensure the video is public
- Scope changed from `youtube.upload` → `youtube` (so the same credentials work for both upload and update)
- `--public` flag replaced with `--private` (public is now the default)
- Added `youtube_set_privacy.py` to pyright exclude list

Now when you upload a video:
```
ww gen-video upload notes/2026-07-20-tesla-p100-vs-m60-for-ai.md output.mp4
```
It will upload as public by default, and explicitly set public after upload succeeds.

For the already-uploaded private video, I still need the video ID to run `ww gen-video set-privacy <video-id> public`. Can you share the video ID from the YouTube URL?
