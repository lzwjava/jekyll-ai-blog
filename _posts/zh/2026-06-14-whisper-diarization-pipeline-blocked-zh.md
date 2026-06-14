---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Whisper说话人分离流水线阻塞
translated: true
type: note
---

明白。以下是上次的情况：

== 总结 ==

1. 创建了 `ww/audio/whisper_diarize.py` — 一个使用 whisperx Python API 的新模块，包含三步流程：转录 → 对齐时间戳 → 使用 pyannote 进行说话人分类。

2. 将其接入 `ww/main.py`，作为 `ww whisper diarize <file>` 命令（与已有的 `ww whisper`、`ww whisper refine`、`ww whisper organize` 并列）。

3. 在 main.py 中添加了帮助文本，并更新了位于 `/home/lzw/projects/ww/completions/_ww` 的 zsh 自动补全。

4. 将 whisperx 安装到 `~/projects/whisper-playground/.venv/`（playground 的虚拟环境，而非 ww 项目的虚拟环境）。

5. 使用 `~/projects/whisper-playground/yangyang/yangyang.mp4` 进行了测试，但遇到阻塞：
   - slower-whisper-large-v3 模型（约 3GB）下载中途不断卡住（网络/代理问题导致无法连接到 HuggingFace CDN）
   - 多次下载到约 2.8GB 后冻结
   - `base` 模型加载正常（较小，约 150MB），证明 CUDA 在 RTX 4070 上可用

6. 会话结束时给出了两个选项：
   A) 使用 aria2c 下载 large-v3（多连接，速度更快）
   B) 使用 `medium` 模型（约 1.5GB，中文准确度仍不错）

   你尚未选择——会话迭代次数已用完。

== 待完成 ==

- 解决 large-v3 模型下载阻塞问题（aria2c 是最干净的方案）
- 对 yangyang.mp4 运行实际的说话人分类
- 验证输出到 yangyang/out/ 目录

需要我接着上次的进度继续吗？我倾向于使用 aria2c 下载 large-v3 —— 这是解决这台机器上 HF 下载卡顿问题的已验证方法。