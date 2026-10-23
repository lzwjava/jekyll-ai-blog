---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 重写README以完全匹配ww工具
translated: true
type: note
---

完成。我已重写 `README.md`，使其完整反映实际的 `ww` 工具，并已根据 `uv run ww` 的帮助输出进行验证。

**主要变更：**

1. **全面覆盖 — 新增 30+ 缺失的命令组**（均已根据工具自身的帮助信息验证）：
   - 新命令组：Help、Actions、AMD Dev Cloud、Appearance、Benchmark、Completion、Cook、Conversation、DB（命令历史）、FFmpeg、Format、GCP Speech、Gen-video、HackerNews、Headphone、Hermes、Host、HuggingFace (hf)、Inference、Keyboard、Maps、Markdown (md2img)、Math、Memory、Monitor、News、Pi、Projects（取代过时的 `update` 命令组）、Qwen、RunPod、SGLang、Torch、Transcript、Vision Model、Weather & Rain、X (Twitter)、Zed

2. **升级现有命令组，补充缺失的子命令**：
   - GitHub：`interests`、`profile`
   - Image：`face`
   - Ghostty：`focus`、`list`
   - Network：`speed`、`physical-speed`、`wifi-scan-best`
   - Linux：`screen-lock`、`switch-keys`
   - Sync：`ww`
   - Note：`--sync`、`--private`、`--code`、`process`、`status`、`clear`、`watch`、`html`
   - Whisper：`--low-memory`、`diarize`、`organize`
   - macOS：`alarm`
   - Screenshot：`--skip-analysis`、`--no-save`、`--area`

3. **准确性修复**：修正了选项默认值（`action` 默认为 gh-pages.yml，`benchmark` 的 SSH 密钥路径，`sglang` 端口，搜索引擎标志等），并添加了带锚点的 `command groups` 索引，便于导航。

通过 `comm` 差异对比验证：README 中的每个命令都存在于实际工具中，且没有遗漏任何实际子命令。
