---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Whisper.cpp音频转录作品
translated: true
type: note
---

whisper.cpp 自身的烟雾测试 — 音频到文本转换。一切正常。

## 1. 基本转录（WAV）

```
./build/bin/whisper-cli -m models/ggml-tiny.en.bin -f samples/jfk.wav
```

```
[00:00:00.000 --> 00:00:07.960]   所以，我的美国同胞们，不要问国家能为你们做什么，
[00:00:07.960 --> 00:00:10.760]   而要问你们能为国家做什么。

加载时间 = 148.84 毫秒 | 编码 = 890.24 毫秒 | 解码 = 38.99 毫秒 | 总计 = 1951.03 毫秒
```

正确的转录，约 1.95 秒处理 11 秒的音频（使用 tiny.en 模型，4 个线程，Vulkan 后端可用但使用 CPU 路径）。

## 2. MP3 输入（miniaudio 解码路径）

```
./build/bin/whisper-cli -m models/ggml-tiny.en.bin -f samples/jfk.mp3 -nt
→ 所以，我的美国同胞们，不要问国家能为你们做什么，而要问你们能为国家做什么。
```

## 3. 输出格式

`-osrt -ovtt -oj -of /tmp/jfk` 产生了有效的 `.srt`、`.vtt`、`.json` 文件：

```
1
00:00:00,000 --> 00:00:07,960
 所以，我的美国同胞们，不要问国家能为你们做什么

2
00:00:07,960 --> 00:00:10,760
 而要问你们能为国家做什么。
```

## 4. 其他标志/示例

| 运行 | 结果 |
| --- | --- |
| `-t 2 -bs 1 -np`（贪婪模式，2 个线程） | 相同文本，片段截断到 8.0/11.0 秒 |
| `-ml 1`（单词时间戳） | 正常 |
| `whisper-vad-speech-segments -vm models/for-tests-silero-v6.2.0-ggml.bin -f samples/jfk.wav` | 检测到 4 个语音片段（0.32–2.27 秒，3.27–4.41 秒，5.38–7.68 秒，8.16–10.62 秒） |

## 注释

- 磁盘上唯一的真实模型是 `models/ggml-tiny.en.bin`（仅英语），因此没有进行多语言/翻译测试；`for-tests-ggml-*.bin` 文件是空桩（它们加载但产生 `""`，正如 CI 预期的那样）。
- 只有 `samples/jfk.wav` / `jfk.mp3` 可用；没有安装 `espeak`/`ffmpeg`/`sox` 来合成额外的音频。
- 工作树保持干净（临时输出写入 `/tmp`）。

结论：音频到文本转换端到端工作正常（WAV + MP3 输入，纯文本/SRT/VTT/JSON 输出，VAD 分段正常）。
