---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复了低内存环境下的Whisper导入错误
translated: true
type: note
---

已修复并验证。以下是完整情况：

## 根本原因

`ww` 作为全局控制台脚本（`/home/lzw/.local/bin/ww`）安装，运行在 **系统 Python 3.11** 下，而机器学习依赖位于项目虚拟环境中。普通的 `ww whisper` 能够工作是因为它调用了系统 Python 中安装的 `whisper` 命令行工具，但 `--low-memory` 会在 **`ww` 解释器内部**执行 `import whisper`——而 openai-whisper 从未在该环境中安装。（`ww whisper diarize` 也存在相同的潜在问题，涉及 `whisperx`。）

## 我的修改

**`ww/audio/whisper_low_mem.py`**——将低内存路径重写为使用 **faster-whisper** 替代 openai-whisper，并添加了一个 `_ensure_deps()` 守卫，如果运行解释器中缺少依赖，则使用项目虚拟环境的 Python 重新执行脚本。命令行接口保持不变（`--model/--language/--task/--device`），新增了 `--compute-type`（auto/float16/int8）和 `--no-proxy`（HF 下载可能会因本地代理而卡住——这与 `diarize` 取消代理设置的原因相同）。仍然像之前一样输出 `.txt/.srt/.vtt/.tsv/.json` 文件。

**`ww/audio/whisper_diarize.py`**——添加了相同的虚拟环境重新执行守卫（否则会以同样的方式崩溃）。

**`ww/main.py`**——更新了 `--low-memory` 的帮助文本。

已通过真实的 `ww` 入口点进行了端到端验证；ruff/pyright 检查通过（仅保留先前存在的发现）。

## 你的问题

**为什么需要 openai-whisper？** 仅用于默认的 `ww whisper` 路径——它调用了你全局安装的 openai-whisper 命令行工具，因此该路径有效。`--low-memory` 不再需要它。

**为什么低内存模式不使用 whisperx？** whisperx 底层其实就是 faster-whisper——它只是 faster-whisper 加上 wav2vec2 词级对齐（额外占用 ~1.2 GB 显存并多一次下载）以及可选的 pyannote 说话人分离（需要 HF token 和模型）。纯转录不需要这些；引擎本身才是节省内存的部分，因此 `--low-memory` 现在直接使用它。当你确实需要说话人标签时，请使用 `ww whisper diarize`。

**注意：** 首次运行时，`large-v3` 模型将从 HuggingFace（`Systran/faster-whisper-large-v3`，约 3 GB）下载——缓存与现有的 `~/.cache/whisper/*.pt` 文件独立。如果下载因代理而卡住，请添加 `--no-proxy`。

提前告知：你对 `ruixiu2.mp4` 首次真正使用 `--low-memory` 时，速度较慢仅是因为模型下载。