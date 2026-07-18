---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ww GCP语音转写音频转录
translated: true
type: note
---

该功能已集成在 `ww` CLI 的 `gcp-speech` 命令组下。使用方式如下：

```
ww gcp-speech transcribe <音频文件> [选项]
```

**参数说明：**

- `<音频文件>` — 音频文件路径（支持 mp3、m4a、wav、ogg、mp4 等格式）
- `--lang LANG` — 语言代码覆盖（默认根据文件名后缀自动检测：`-zh`/`-cn` 为中文，其余为英文）
- `--wait` — 等待任务完成并下载结果（默认为异步模式：提交任务后打印控制台链接并退出）

**使用示例：**

```sh
ww gcp-speech transcribe ~/Downloads/recording.mp3
ww gcp-speech transcribe ~/Downloads/recording-zh.mp3 --lang cmn-Hans-CN
ww gcp-speech transcribe ~/Downloads/long.mp3 --wait
```

该功能会将音频上传至 GCS（`test2x` 存储桶），通过 Google Cloud Speech-to-Text v2 提交批量任务，然后打印控制台链接（异步模式）或轮询结果并在音频文件旁保存 `.md` 格式的转录文本（`--wait` 模式）。
