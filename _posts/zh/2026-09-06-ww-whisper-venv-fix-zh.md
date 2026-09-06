---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Whisper venv 修复
translated: true
type: note
---

已修复并验证。以下是完整故事：

## 问题描述

`ww whisper` 是对 **faster-whisper**（CTranslate2 后端）的封装，但它运行在 **系统 python3.11** 环境下（`/usr/bin/python3.11`，根据 `ww` 控制台脚本的 shebang 行），该环境在 `~/.local/lib/python3.11/site-packages` 中有自己独立的 ML 栈：
- `ctranslate2 4.5.0` — **旧版本**。其运行时通过版本化名称加载 cuDNN（如 `libcudnn_ops.so.9.1.0` 等），但找不到所需的 cuDNN 布局，随后报错：
  `Unable to load any of {...}` → `Invalid handle. Cannot load symbol cudnnCreateTensorDescriptor` → `Aborted (core dumped)`
- `faster-whisper 1.0.3` — 也已过时

你的项目虚拟环境（`/home/lzw/projects/ww/.venv`）中包含了 **可正常工作的固定版本** —— `ctranslate2 4.8.0`（无损坏的 cuDNN 依赖）+ `faster-whisper 1.2.1`。我确认了完全相同的转录任务在 `.venv/bin/python` 下能正常运行，而通过 `ww` 封装就会崩溃。

**为何封装未使用虚拟环境：** whisper 脚本中的 `_ensure_deps()` 辅助函数只在模块 *缺失* 时才重新执行到虚拟环境。你的系统 Python 中 *存在* 这些包——只是版本过旧——因此它静默地使用了有问题的 4.5.0 版本。（崩溃仅在语言检测后的解码过程中出现，这就是为什么它看起来很奇怪。）

## 修复（在 `/home/lzw/projects/ww` 目录下）

修改了 `ww/audio/whisper_translate.py`、`whisper_low_mem.py` 和 `whisper_diarize.py` 中的 `_ensure_deps()` 函数，使其 **始终优先使用项目 `.venv`**，除非已经在其中运行（通过 `sys.prefix` 检测）。同时：
- 在 `whisper_translate.py` 中添加了缺失的 `if __name__ == "__main__": main()` 保护（其旧的重新执行约定通过控制台脚本运行，因此模块无法直接执行——现在重新执行像其他两个脚本一样直接指向模块文件）。
- 每次重新执行时，会向 stderr 输出 `[ww] Re-running with project venv python: ...` 以增加透明度。

## 验证结果

- `ww whisper clip.mp3 --language zh` —— 之前崩溃，现在正常转录。
- `ww whisper --low-memory --model tiny` —— 同样的旧依赖 bug，现已修复。
- `ww whisper diarize` 原本就能工作（whisperx 在系统 Python 中缺失，强制使用虚拟环境），不受影响。

你现在可以直接重新运行原始命令：
```
ww whisper daniel.mp3 --language zh
```

可选的清理（目前非必需）：如果你不希望将来系统 Python 的旧副本干扰，可以卸载 `~/.local/lib/python3.11/site-packages` 中的 `faster-whisper`/`ctranslate2`——但优先使用虚拟环境的逻辑现在已能保护你。