---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Whisper模型重新下载期间的下载速度
translated: true
type: note
---

问题：如何理解在RTX 4070上Whisper large-v3模型重新下载进度中显示的速度？

答案：

## 实际情况

你看到的是**并非GPU转录速度**——而是**模型文件重新下载**。原因如下：

```
UserWarning: /home/lzw/.cache/whisper/large-v3.pt exists,
but the SHA256 checksum does not match; re-downloading the file
```

之前缓存的 `large-v3.pt` 文件**损坏或不完整**，因此Whisper正在从互联网重新下载它。`6.42 MiB/s` 是你的**互联网下载速度**，而非GPU速度。

---

## 解析进度条

```
38%|████████████████                     | 1.09G/2.88G [01:45<04:57, 6.42MiB/s]
```

| 字段 | 值 | 含义 |
| --- | --- | --- |
| `38%` | 进度 | 已下载文件的38% |
| `1.09G / 2.88G` | 字节 | 已下载1.09 GB，总大小2.88 GB |
| `01:45` | 已用时 | 已用时1分45秒 |
| `04:57` | 剩余时间 | 约5分钟剩余 |
| `6.42 MiB/s` | 速度 | 约6.42 MB/s的互联网下载速度 |

`large-v3` 模型文件大小为**2.88 GB**——这是完整的模型权重检查点。

---

## 下载完成后该做什么

下载完成后，Whisper将在你的**RTX 4070**上开始实际转录，这款GPU非常适合该任务。基准测试表明，在同类GPU中，RTX 4070在Whisper转录方面拥有最佳性价比。

使用 `large` 模型在RTX 4070上，你可以预期大约**15–30倍的实时速度**（例如，一个60分钟的音频文件在2–4分钟内完成转录）。

---

## 如何避免下次出现此问题

校验和不匹配通常意味着之前的下载中断。为避免重新下载：

1. **让下载完整完成**，不要中断。
2. 或者手动预下载模型并验证完整性：

```bash
# 下载后检查文件是否完整
ls -lh ~/.cache/whisper/large-v3.pt
# 应该约为2.88 GB
```

---

## 额外建议：使用 `faster-whisper` 获得更佳速度

如果你希望在RTX 4070上获得显著更快的转录速度，可以考虑切换到 `faster-whisper`：

```bash
pip install faster-whisper
```

Faster-whisper 使用CTranslate2，在加载时可按大小自动从Hugging Face Hub下载模型，并支持 `float16` 量化以实现更好的GPU性能。

参考：

- [不同GPU的性能基准测试 · openai/whisper · 讨论 #918](https://github.com/openai/whisper/discussions/918)
- [GitHub - SYSTRAN/faster-whisper](https://github.com/SYSTRAN/faster-whisper)
