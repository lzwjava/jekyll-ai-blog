---
audio: false
generated: true
image: false
lang: zh
layout: post
title: YouTube上传隐私更新
translated: true
type: note
---

已完成。以下是我提交并推送到 `main` 分支的 2 个提交：

**提交 1** — `7bd9257`: 新增 `ww gen-video set-privacy` 命令

- 新命令：`ww gen-video set-privacy <video_id> <public|unlisted|private>`
- 使用 `youtube` 权限范围，令牌缓存在 `~/.google/youtube_update_token.json`
- 获取当前视频状态，仅更新隐私设置字段

**提交 2** — `5a3e258`: 上传后自动设为公开

- 默认隐私设置从 `private` 改为 `public`
- 上传成功后，显式调用更新 API 以确保视频公开
- 权限范围从 `youtube.upload` 改为 `youtube`（这样同一份凭据即可同时用于上传和更新）
- `--public` 标记替换为 `--private`（现在默认是公开）
- 将 `youtube_set_privacy.py` 添加到 pyright 排除列表

现在当你上传视频时：

```
ww gen-video upload notes/2026-07-20-tesla-p100-vs-m60-for-ai.md output.mp4
```

它将默认以公开状态上传，并在上传成功后显式设置为公开。

对于已经上传的私有视频，我仍然需要视频 ID 来运行 `ww gen-video set-privacy <video-id> public`。你能分享 YouTube URL 中的视频 ID 吗？
