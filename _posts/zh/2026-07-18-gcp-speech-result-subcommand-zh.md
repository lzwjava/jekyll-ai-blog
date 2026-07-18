---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GCP 语音结果子命令
translated: true
type: note
---

所有更改已就位。以下是所做工作的摘要：

**所做的更改：**

1. **`ww/gcp_speech/result.py`**（新文件）—— `ww gcp-speech result <job-id>` 命令：
   - 在 `~/.ww_gcp_jobs.json`（本地作业注册表）中查找作业 ID
   - 检查 GCS 中是否已完成转录 JSON 文件
   - 如果结果存在：下载结果，打印转录文本，并将 `.md` 文件保存到原始音频旁边
   - 如果尚未完成：打印控制台 URL 并建议使用 `--wait` 进行轮询
   - 支持 `--wait` 标志用于阻塞模式（每 10 秒轮询一次）

2. **`ww/gcp_speech/transcribe.py`** — 修改为：
   - 在输出中打印清晰的 `Job ID:` 行（即基本名称/文件名主干）
   - 将作业信息保存到 `~/.ww_gcp_jobs.json`（操作名称、GCS 文件夹、音频文件、语言）
   - 引导用户使用 `ww gcp-speech result <job-id> --wait` 代替 `gsutil cp`

3. **`ww/main.py`** — 添加了 `result` 子命令路由和帮助文本

4. **`~/.zsh/completions/_ww`** — 将 `result` 添加到 `gcp_speech_cmds` 中，用于 Tab 补全

**使用流程：**
```
ww gcp-speech transcribe ~/Downloads/recording.mp3
  → 输出：Job ID: recording
  → 将作业保存到 ~/.ww_gcp_jobs.json

ww gcp-speech result recording
  → 检查 GCS 中是否有结果，如果就绪则打印转录文本

ww gcp-speech result recording --wait
  → 轮询直到完成，然后打印转录文本
```