---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: SRS 开源流媒体服务器
translated: true
type: note
---

Question: 请全面介绍一下 SRS 这个 Simple RTMP Streaming 开源项目。

Answer:

**SRS (Simple Realtime Server)** 是目前最受欢迎且应用最广泛的**开源实时媒体流服务器**之一。

它最初主要作为一个高性能的 **RTMP server** 启动，但现已演变为一个功能强大、支持全协议的实时流媒体网关。

### 基本信息

- **全称**：Simple Realtime Server（最初侧重于 RTMP）
- **License**：MIT（非常宽松的开源许可）
- **主仓库**：https://github.com/ossrs/srs
- **官方网站**：https://ossrs.net/
- **主要语言**：C++（包含部分辅助脚本和工具）
- **当前状态 (2026)**：项目非常活跃，被许多公司（尤其是中国公司）广泛用于生产环境，并持续添加现代流媒体特性。

### 核心特性

SRS 在单个进程中支持丰富的流媒体协议：

- **经典协议**
  - RTMP (push & pull)
  - HTTP-FLV (在中国非常流行)
  - HTTP-TS
  - HLS (Apple HTTP Live Streaming)

- **现代超低延迟协议**
  - WebRTC (自 2020–2021 年以来非常重要)
  - SRT (Secure Reliable Transport)

- **其他重要协议**
  - MPEG-DASH
  - GB28181 (对中国国家标准安防监控摄像头非常重要)

### 典型延迟对比（良好网络条件下的近似值）

| Protocol | Typical Latency | Use Case |
| :--- | :--- | :--- |
| RTMP | 2–5 seconds | 传统直播 (OBS → 类似 YouTube/Twitch) |
| HLS | 5–30 seconds | 广泛的兼容性，类似 VOD |
| HTTP-FLV | 2–5 seconds | Flash 时代的替代品，在亚洲浏览器中非常流行 |
| WebRTC | 0.3–1.0 second | 互动直播、游戏、拍卖、监控 |
| SRT | 0.5–2 seconds | 贡献端 / 劣质网络上的低延迟传输 |

### 使用 SRS 的常用架构模式

1.  **最简单的 RTMP server**（大多数人从这里开始）
    ```
    OBS/FFmpeg → RTMP → SRS → HLS/HTTP-FLV/WebRTC → viewers
    ```

2.  **低延迟分发**
    ```
    OBS → RTMP → SRS → WebRTC → browser (sub-second latency)
    ```

3.  **Edge + Origin cluster（边缘 + 源站集群）**
    ```
    Many edge SRS (HTTP-FLV/WebRTC) ← cluster pull ← origin SRS (ingest RTMP/SRT/GB28181)
    ```

4.  **WebRTC ↔ RTMP 转换**
    SRS 可以在 WebRTC 和 RTMP 之间进行双向转换。

### SRS 的主要优势

- **高性能** —— 单个进程可以处理数千个并发流。
- **极低的内存占用** —— 与许多替代方案相比，内存消耗极低。
- **出色的稳定性** —— 在长期运行的生产环境中表现优异（许多服务器运行数年无需重启）。
- **非常活跃的中文社区** —— 大多数 Issue/PR/文档都有中文，且英文支持也在不断改进。
- **Docker 镜像维护良好** —— 并且被广泛使用。
- **跨平台** —— 可以在几乎所有的 Linux 发行版上编译运行，并对 ARM64 有良好的支持。

### 谁在利用 SRS？

- 许多中国直播平台（部分斗鱼、虎牙、Bilibili 的基础设施灵感来源）。
- 视频监控公司（尤其是对 GB28181 的支持）。
- 中小型直播初创公司。
- 教育和教堂直播设置。
- 许多希望在不使用商业 CDN 的情况下实现亚秒级延迟的开发者。

### 快速入门 (2026 年最常用的方式)

```bash
# 最快的方式 - Docker
docker run --rm -it -p 1935:1935 -p 1985:1985 -p 8080:8080 ossrs/srs:5
```

然后推送流：

```bash
ffmpeg -re -i test.mp4 -c copy -f flv rtmp://localhost/live/livestream
```

播放：

- HLS: http://your-ip:8080/live/livestream.m3u8
- HTTP-FLV: http://your-ip:8080/live/livestream.flv
- WebRTC: 使用 http://your-ip:8080/ 上的演示播放器

当你需要一个开源、高性能、多协议的实时流媒体服务器时，SRS 仍然是最佳选择之一 —— 尤其是当你需要在同一个盒子里实现 **RTMP ingestion + WebRTC/HLS delivery** 时。

References:

- [SRS Official Website](https://ossrs.net/lts/en-us)
- [SRS GitHub Repository](https://github.com/ossrs/srs)
- [SRS Introduction Documentation](https://ossrs.net/lts/en-us/docs/v6/doc/introduction)
