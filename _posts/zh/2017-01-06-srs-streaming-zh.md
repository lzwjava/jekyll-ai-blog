---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 简单实时服务器（SRS）用于RTMP流媒体
translated: true
type: post
---

让我们深入了解如何使用 Simple Realtime Server (SRS) 部署边缘服务器进行 RTMP 流媒体传输，重点是理解和有效配置它，包括 `rtmp.conf` 文件。SRS 是一个功能强大、高性能的媒体服务器，专为实时流媒体协议如 RTMP、HLS 和 HTTP-FLV 设计。它特别适用于需要可扩展性的场景，例如内容分发网络（CDNs），边缘服务器可以高效地将流分发给许多客户端，同时从源服务器获取内容。我将一步一步地带你完成这个过程，解释边缘部署的概念，并说明如何处理 `rtmp.conf` 等配置。

### 什么是 SRS 和边缘部署？
SRS 是一个开源服务器，专为处理实时媒体流媒体而设计，注重简洁和高效。它支持 RTMP（实时消息传输协议）用于低延迟的实时流媒体，以及其他协议如 HLS 和 WebRTC。在 SRS 中，边缘服务器充当客户端（观众或发布者）和源服务器（流的来源）之间的中介。边缘服务器仅在客户端请求时从源服务器获取流，从而减轻源服务器的负担，并实现可扩展的分发——可以将其视为为实时流量定制的 CDN 缓存层。

在 SRS 上部署边缘服务器是理想的，当你需要：
- 为大量观众提供服务而不压垮源服务器。
- 允许发布者将流推送到边缘，然后由边缘转发到源服务器。
- 通过利用更便宜的边缘节点来最小化昂贵源服务器的带宽使用。

### 逐步部署 SRS 进行 RTMP 流媒体的边缘服务器
以下是如何在 Linux 系统（例如 Ubuntu）上将 SRS 设置为 RTMP 流媒体的边缘服务器。假设你正在使用 Linux 系统，因为 SRS 为这种环境进行了优化。

#### 1. 安装 SRS
首先，你需要在机器上运行 SRS：
- **下载 SRS**：从官方 GitHub 仓库获取最新稳定版本（github.com/ossrs/srs）。截至 2025 年 2 月 26 日，你通常会克隆该仓库：
  ```
  git clone https://github.com/ossrs/srs.git
  cd srs
  ```
- **构建 SRS**：SRS 使用简单的构建过程 `./configure` 和 `make`：
  ```
  ./configure
  make
  ```
  这将编译服务器到 `objs` 目录（例如 `objs/srs`）。
- **测试二进制文件**：使用默认配置运行它，以确保其工作正常：
  ```
  ./objs/srs -c conf/srs.conf
  ```
  默认情况下，它在端口 1935 上监听 RTMP。检查控制台输出以确认。

#### 2. 理解边缘概念
在 SRS 中，边缘服务器以“远程”模式运行，这意味着它不生成流，而是在客户端请求时从源服务器拉取流（用于播放）或将流推送到源服务器（用于发布）。这种按需获取是边缘服务器高效扩展 RTMP 传输的原因。

- **源服务器**：流的来源（例如，编码器如 OBS 将 RTMP 流推送到的位置）。
- **边缘服务器**：客户端连接的中继，仅在需要时从源服务器获取。

对于这个示例，假设你已经在 `192.168.1.100:1935` 上运行了一个源服务器（将此替换为你的实际源 IP）。

#### 3. 配置边缘服务器
SRS 使用配置文件来定义其行为。默认的 `srs.conf` 是一个很好的起点，但对于边缘部署，你将创建一个特定的配置文件——我们称之为 `edge.conf`。以下是如何设置它：

- **创建 `edge.conf`**：
  ```
  cd conf
  nano edge.conf
  ```
- **添加边缘配置**：
  这是一个用于 RTMP 边缘部署的最小 `edge.conf`：
  ```conf
  listen              1935;
  max_connections     1000;
  srs_log_tank        file;
  srs_log_file        ./objs/edge.log;
  vhost __defaultVhost__ {
      cluster {
          mode        remote;
          origin      192.168.1.100:1935;
      }
  }
  ```
  - `listen 1935`：边缘监听 RTMP 连接的端口 1935。
  - `max_connections 1000`：限制并发连接（根据你的服务器容量进行调整）。
  - `srs_log_file`：记录到文件以进行调试。
  - `vhost __defaultVhost__`：默认虚拟主机配置。
  - `cluster { mode remote; origin 192.168.1.100:1935; }`：将此服务器设置为边缘（`mode remote`）并指向源服务器。

- **保存并退出**：在 nano 中按 Ctrl+O，Enter，Ctrl+X。

#### 4. 启动边缘服务器
使用你的边缘配置运行 SRS：
```
./objs/srs -c conf/edge.conf
```
检查日志（`./objs/edge.log`）以确认它正在运行并连接到源服务器。

#### 5. 测试设置
- **发布流**：使用 OBS 或 FFmpeg 将 RTMP 流推送到源服务器：
  ```
  ffmpeg -re -i input.mp4 -c copy -f flv rtmp://192.168.1.100/live/livestream
  ```
  这里，`live` 是应用程序名称，`livestream` 是流密钥。
- **从边缘播放**：使用 VLC 或其他 RTMP 客户端从边缘播放流：
  ```
  rtmp://<edge-server-ip>/live/livestream
  ```
  将 `<edge-server-ip>` 替换为你的边缘服务器的 IP（例如 `192.168.1.101`）。边缘将从源服务器获取流并为你提供服务。

#### 6. 探索 `rtmp.conf`
SRS 默认不附带 `rtmp.conf` 文件，但在教程或自定义设置中可能会遇到对它的引用。它本质上是一个用于 RTMP 特定配置文件的命名约定。例如，SRS 文档（ossrs.net）提供了一个用于实时 RTMP 流媒体的示例 `rtmp.conf`：
```conf
listen              1935;
max_connections     1000;
vhost __defaultVhost__ {
    tcp_nodelay     on;
    min_latency     on;
    play {
        gop_cache   off;
        queue_length 10;
    }
    publish {
        mr          off;
    }
}
```
- **用途**：此配置优化了源服务器的低延迟 RTMP 流媒体，而不是边缘。对于边缘部署，你可以通过添加步骤 3 中的 `cluster` 块来适应它。
- **关键设置**：
  - `tcp_nodelay on`：通过禁用 Nagle 的算法来减少延迟。
  - `min_latency on`：优先考虑低延迟而非缓冲。
  - `gop_cache off`：禁用组图像缓存以进行实时播放。
  - `mr off`：禁用“合并读取”以避免发布延迟。

对于边缘，你可以将其与 `cluster` 设置结合使用，而不是单独使用它。

### 进一步解释：边缘机制和 RTMP
- **边缘工作原理**：当客户端请求 `rtmp://<edge-ip>/live/livestream` 时，边缘检查是否有流。如果没有，它将从源服务器（`192.168.1.100:1935`）拉取并本地缓存以供其他客户端使用。如果发布者将流推送到边缘，它将流转发到源服务器。
- **RTMP 详细信息**：RTMP 是一种适合实时流媒体的低延迟协议。SRS 高效处理 RTMP，支持绝对时间编码（ATC）以跨服务器同步，但在边缘模式下默认关闭，除非指定。
- **可扩展性**：添加多个指向同一源服务器的边缘以处理数千个客户端。SRS 支持故障转移，通过列出多个源（例如 `origin 192.168.1.100:1935 192.168.1.200:1935;`）。

### 技巧和故障排除
- **防火墙**：确保源服务器和边缘服务器上的端口 1935 打开。
- **日志**：检查 `edge.log` 中的错误，例如与源服务器的连接失败。
- **延迟**：如果源服务器延迟低，边缘添加的延迟通常小于 1 秒。
- **多个边缘**：部署具有相同配置的额外边缘，根据需要调整 `listen` 端口或 IP。

### 总结
部署 SRS 边缘服务器进行 RTMP 流媒体传输是一旦理解源-边缘关系后就变得简单。`edge.conf` 设置边缘以动态获取或推送流，而 `rtmp.conf` 样式的配置可以根据需要进一步优化 RTMP 性能。使用此设置，你已经准备好高效地扩展实时流媒体传输——无论是为少量观众还是全球观众。想进一步调整它或将 HLS 与 RTMP 集成？告诉我！
