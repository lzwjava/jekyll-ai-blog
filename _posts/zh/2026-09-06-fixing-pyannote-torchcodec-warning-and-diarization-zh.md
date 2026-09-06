---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复Pyannote Torchcodec警告与说话人日志
translated: true
type: note
---

已修复。以下是该警告的完整情况以及我所做的修改。

## 根本原因

该警告并非 whisperx 的问题——而是 pyannote.audio ≥ 4 尝试导入 **torchcodec**（其音频解码器）失败所致：

- torchcodec 0.7.0 已安装，且是与 torch 2.8.0 兼容的正确版本。它为每个 FFmpeg 主版本（4-7）提供一组 `.so` 文件。在你的机器上，FFmpeg-6 变体与系统库 `libav*` 匹配，且其核心 + pybind 库加载正常——但其 **自定义操作库也链接了 `libpython3.11.so.1.0`**，而该文件在本机任何位置都不存在（`/usr/bin/python3.11` 是 Ubuntu 的*静态* ESM 构建版本，未安装 `libpython3.11`/`-dev` 包）。因此 torchcodec 拒绝加载，pyannote 每次运行时都会打印出那个吓人的警告。
- 对于 `ww whisper diarize` 来说，这只是*表面问题*（whisperx 会将音频预加载到内存中，因此 pyannote 从不通过路径解码），但这也意味着如果任何代码路径需要解码音频，pyannote 将无法真正解码音频文件。

## 所做的修改（`ww/audio/whisper_diarize.py`，+88/−9）

1. **torchcodec 现在可以加载**——`_prepend_libpython_dir()` 会在 uv/pyenv 管理的 Python 目录下定位 ABI 兼容的 `libpython3.11.so.1.0`，并将其添加到 `LD_LIBRARY_PATH` 中，然后重新执行进入虚拟环境。我通过 `uv python install 3.11` 安装了一个（位于 `~/.local/share/uv/python/cpython-3.11.15-.../lib`）。已验证：pyannote 可零警告导入，并能通过 torchcodec 解码 mp3。
2. **说话人分离静默跳过了**——你之前的运行打印了 `[1/2]`，而不是 `[1/3]`：脚本仅在设置了 `HF_TOKEN` 时才执行说话人分离，但该变量未设置（你实际上已通过 `~/.cache/huggingface/token` 登录）。现已回退使用该缓存令牌。
3. **代理被禁用**——`_disable_proxy()` 无条件执行，但本机**没有直达 huggingface.co 的路由**（只能通过 `127.0.0.1:7890` 代理），因此模型下载因“网络不可达”而失败。代理处理现已改为通过 `--no-proxy` 选择加入（与 `whisper_low_mem.py` 的惯例一致）。
4. **`--diarize-model` 参数传递**——whisperx 3.8.6 硬编码了 `pyannote/speaker-diarization-community-1`；现在你可以指向 `pyannote/speaker-diarization-3.1`。

已在一个 20 秒的音频片段上进行了端到端验证：无 torchcodec 警告，令牌自动检测（`[1/3]`），转录运行正常，说话人分离通过代理成功连接 Hugging Face。

## 唯一需要你处理的事情

剩余的障碍是 **受门控的 HF 仓库**（返回 403 错误，非代码问题）。你的缓存令牌未被授权访问 pyannote 模型，因此请使用与 `~/.cache/huggingface/token` 相同的账户（令牌以 `hf_m...` 开头）在浏览器中登录并接受访问权限：

- <https://huggingface.co/pyannote/speaker-diarization-community-1（whisperx> 的默认模型——**此模型是必需的**；pyannote 的 3.1 管道也会从此处拉取其 xvec/PLDA 资源）
- <https://huggingface.co/pyannote/segmentation-3.0（底层分割模型）>
- <https://huggingface.co/pyannote/speaker-diarization-3.1（仅在使用> `--diarize-model` 时需要）

然后只需再次运行：

```
ww whisper diarize daniel.mp3
```

日志中的 `TF32` 可重现性警告和 Lightning “检查点升级”通知是无害的 pyannote 噪音，可以忽略。
