---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: SRS Open Source Streaming Server
translated: false
type: note
---

Question: Give a comprehensive introduction to SRS, the Simple RTMP Streaming open-source project.

Answer: 

**SRS (Simple Realtime Server)** is one of the most popular and widely used **open-source real-time media streaming servers**.  

It started primarily as a high-performance **RTMP server** but has evolved into a very capable, all-protocol real-time streaming gateway.

### Basic Information
- **Full name**: Simple Realtime Server (originally focused heavily on RTMP)
- **License**: MIT (very permissive open-source license)
- **Main repository**: https://github.com/ossrs/srs
- **Official website**: https://ossrs.net/
- **Primary language**: C++ (with some scripts and tools in other languages)
- **Current status (2026)**: Very active project, widely used in production by many companies (especially in China), and continuously adding modern streaming features

### Core Features
SRS supports a rich set of streaming protocols in one single process:

- **Classic protocols**
  - RTMP (push & pull)
  - HTTP-FLV (very popular in China)
  - HTTP-TS
  - HLS (Apple HTTP Live Streaming)

- **Modern ultra-low latency protocols**
  - WebRTC (very important since ~2020–2021)
  - SRT (Secure Reliable Transport)

- **Other important protocols**
  - MPEG-DASH
  - GB28181 (very important for Chinese national standard surveillance cameras)

### Typical Latency Comparison (approximate values in good network conditions)

| Protocol       | Typical Latency | Use Case                              |
|----------------|------------------|---------------------------------------|
| RTMP           | 2–5 seconds     | Traditional live streaming (OBS → YouTube/Twitch-like) |
| HLS            | 5–30 seconds    | Broad compatibility, VOD-like         |
| HTTP-FLV       | 2–5 seconds     | Flash-era replacement, very popular in browsers in Asia |
| WebRTC         | 0.3–1.0 second  | Interactive live, gaming, auction, surveillance |
| SRT            | 0.5–2 seconds   | Contribution / low-latency transport over bad networks |

### Common Architecture Patterns Using SRS
1. **Simplest RTMP server** (most people start here)
   ```
   OBS/FFmpeg → RTMP → SRS → HLS/HTTP-FLV/WebRTC → viewers
   ```

2. **Low-latency delivery**
   ```
   OBS → RTMP → SRS → WebRTC → browser (sub-second latency)
   ```

3. **Edge + Origin cluster**
   ```
   Many edge SRS (HTTP-FLV/WebRTC) ← cluster pull ← origin SRS (ingest RTMP/SRT/GB28181)
   ```

4. **WebRTC ↔ RTMP conversion**
   SRS can convert between WebRTC and RTMP in both directions.

### Key Advantages of SRS
- Very **high performance** — single process can handle thousands of concurrent streams
- Extremely **low memory usage** compared to many alternatives
- Excellent **stability** in long-running production (many servers run for years without restart)
- Very active Chinese community (most issues/PRs/docs in Chinese, but English support improving)
- Docker images are well maintained and widely used
- Can compile & run on almost all Linux distributions, and has good ARM64 support

### Who Uses SRS?
- Many Chinese live streaming platforms (parts of Douyu, Huya, Bilibili infrastructure inspiration)
- Video surveillance companies (especially GB28181 support)
- Small/medium live streaming startups
- Educational & church live streaming setups
- Many developers who want sub-second latency without commercial CDNs

### Quick Start (most common way in 2026)
```bash
# Fastest way - Docker
docker run --rm -it -p 1935:1935 -p 1985:1985 -p 8080:8080 ossrs/srs:5
```

Then push stream:
```bash
ffmpeg -re -i test.mp4 -c copy -f flv rtmp://localhost/live/livestream
```

Play:
- HLS: http://your-ip:8080/live/livestream.m3u8
- HTTP-FLV: http://your-ip:8080/live/livestream.flv
- WebRTC: use the demo player on http://your-ip:8080/

SRS remains one of the best choices when you want an open-source, high-performance, multi-protocol real-time streaming server — especially if you need **RTMP ingestion + WebRTC/HLS delivery** in the same box.

References:  

- [SRS Official Website](https://ossrs.net/lts/en-us)
- [SRS GitHub Repository](https://github.com/ossrs/srs)
- [SRS Introduction Documentation](https://ossrs.net/lts/en-us/docs/v6/doc/introduction)