---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 新增 ll video 子命令
translated: true
type: note
---

所有内容都已提交并推送——`main` 现在与 `origin/main` 同步。

## 摘要：新增 `ll video`

**新文件：**
- `src/video_ops.rs`（约 1450 行）— 18 条命令 + 21 个单元测试
- `src/cli.rs` — 共享的标志/位置参数解析，现已被 `image` 和 `video` 模块共同使用

**修改：** `src/main.rs`（分发）、`src/image_ops.rs`（使用共享 CLI 辅助函数）、`README.md`（Video tools 部分）

### 命令

| 分组 | 命令 |
|---|---|
| 检查 | `info <file>…`（流、编解码器、fps、`--json`） |
| 剪切与拼接 | `screenshot`、`frames`（`--fps`/`--every` 序列）、`trim`（流复制 / `--reencode`）、`concat`、`reverse` |
| 音频 | `audio`（按扩展名支持 mp3/m4a/wav/flac/opus）、`mute`、`volume`（`-v 0.5` / `-v -6dB`） |
| 变换 | `resize`、`crop`、`rotate`、`flip`、`speed`（音频通过链式 `atempo` 跟随） |
| 导出 | `convert`（h264/hevc/vp9/av1/copy + `--crf`/`--preset`/`--fps`）、`gif`（调色板优化）、`gif2video`、`sprite`（接触表） |

### 设计说明

- **ffmpeg/ffprobe 驱动** — 纯 Rust 转码不现实；该模块调用外部命令，但每条命令都会**回显它运行的精确 ffmpeg 命令行**，`--dry-run` 只打印而不执行。缺少二进制文件时会产生友好的安装提示。
- **纯构建器函数** — `build_trim`、`build_screenshot`、`atempo_chain`、`parse_crop_geometry` 等与 I/O 解耦，因此参数构造可以在不接触 ffmpeg 的情况下进行单元测试。
- **便利性**：时间接受 `90` / `1:30` / `01:02:03.5`，输出目录自动创建，容器编解码器按扩展名选择，负数解析为数值。

**验证：** `cargo build` 无警告，**38/38 测试通过**，所有新代码均通过 clippy，并对真实生成的视频进行了完整的端到端运行（使用 `ffprobe` 验证时长/尺寸），以及 image↔video 回归检查。

已推送的提交：
```
3c79248 feat: add video subcommand with common operations (ffmpeg-backed)
```