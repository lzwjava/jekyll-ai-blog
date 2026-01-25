---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Google Cloud Live Stream API 概览
translated: true
type: note
---

**Question:** Google Cloud 是否有类似于阿里云直播的服务，可以提供推流 URL，并允许客户端通过 HLS 或 RTMP 进行拉流观看？

**Answer:** 

是的，Google Cloud 提供了一项名为 **Live Stream API** 的专用直播服务（属于 Google Cloud 媒体服务的一部分），其功能与阿里云（Aliyun）视频直播非常相似。

### 核心功能及工作原理：

- **Ingest (推流)**：  
  你在 Live Stream API 中创建一个 **input endpoint**。  
  它支持 **RTMP**（以及 SRT）作为输入协议。  
  Google Cloud 会提供一个 **RTMP ingest URL**（例如：rtmp://[endpoint]/live）和 **stream key**，供你使用 OBS、FFmpeg 或硬件编码器推送直播流 —— 这与阿里云的推流 URL 机制完全一致。

- **Processing (处理)**：  
  该服务会将输入的直播信号（贡献级质量）转码为自适应比特率（adaptive bitrate）推流格式。

- **Output / Playback (下行播放)**：  
  它生成 **HLS** (HTTP Live Streaming) 和 **DASH** 输出流。  
  你会获得 HLS 的播放 URL（常用于 Web/移动端播放器），客户端可以使用该 URL 进行观看。  
  RTMP 仅支持 **input (推流)**，而输出/播放主要采用 HLS/DASH（现代低延迟自适应流媒体协议）。通常不提供 RTMP 播放输出，因为它正逐渐被 HLS/DASH/WebRTC 等更广泛的用例所取代。

- **与阿里云直播的对比**：
  - 两者都提供用于推流的 RTMP/SRT ingest URL 和 Key。
  - 两者都会进行转码并交付自适应流。
  - 阿里云在某些遗留场景中仍强调 RTMP 播放，但现代播放器（包括阿里云自带的播放器）已大量使用 HLS/FLV over HTTP。Google Cloud 专注于 HLS/DASH，这是目前广泛兼容性（浏览器、iOS、Android 等）的行业标准。
  - 如果你明确需要 RTMP 播放输出，Google Cloud 的 Live Stream API 原生并不提供（你需要通过自己的服务器等方式单独处理），但 HLS 是推荐且完全支持的观看方式。

该服务是全托管、可扩展的，并与 Media CDN、Cloud Storage 等其他 Google Cloud 产品集成，以实现全球低延迟交付。

欲了解更多详情，请查看官方文档。

**References:**  

- [Overview of the Live Stream API](https://docs.cloud.google.com/livestream/docs/overview)
- [Live Stream API documentation](https://docs.cloud.google.com/livestream/docs)