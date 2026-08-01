---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Whisper低内存模块已接线
translated: true
type: note
---

全部完成。`ww whisper <file> --low-memory` 已连接。变更总结：

## 变更

**1. 新增模块 — `ww/audio/whisper_low_mem.py`**
将您的 `transcribe.py` 内存安全加载器（CPU 检查点 → 仅 GPU fp16，large-v3 约 3.2 GB）适配为规范的 `main()` 模块。`whisper` 采用延迟导入，如果未安装 `openai-whisper` 则会显示友好的错误提示。命令行接口：
```
ww whisper file.mp4 --low-memory [--model large-v3] [--language zh] [--task transcribe|translate] [--device cuda]
```
会在音频文件旁生成 `<stem>.txt/.srt/.json/.vtt/.tsv` 文件，与您的脚本一致。

**2. `ww/main.py`**
- 路由：`argv` 中任意位置的 `--low-memory` 会被剥离并分发至 `whisper_low_mem`（在默认的 `whisper_translate` 回退处理之前）。
- 帮助文本：在 Whisper 部分下方增加了 `ww whisper <file> --low-memory` 行。

**3. `~/.zsh/completions/_ww`**
`whisper` 文件补全现在也支持 `--low-memory`、`--model`、`--language`、`--task`、`--device` 参数。（使用 `autoload -Uz compinit && compinit` 重新加载。）

**4. `pyproject.toml`**
添加了 `openai-whisper>=20240930` — 已运行 `uv sync`，干净地安装了 `openai-whisper==20250625`（torch 已通过 whisperx 存在）。

## 已验证
- `uv run ruff check` — 通过；`pyright` — 0 个错误
- `uv run ww whisper --low-memory` — 路由正确（argparse 显示新模块的使用说明）
- 缺失文件错误路径工作正常
- `zsh -n` 补全语法检查通过

注意：模型必须缓存在 `~/.cache/whisper/large-v3.pt`（使用 `whisper large-v3` 下载一次）；如果缺失，加载器会提示。完整的转录流程需要您的 CUDA GPU，请在工作站上进行测试。