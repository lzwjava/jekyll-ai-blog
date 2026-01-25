---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 配置 SRS 源站和边缘服务器
translated: true
type: note
---

**Question:** 在 SRS (Simple RTMP Server) 中，如何配置 edge 节点和 main (origin) 节点？

**Answer:**

在 SRS (Simple RTMP Server) 中，**main endpoint** 通常被称为 **origin server**（源站），而 **edge endpoint** 即为 **edge server**（边缘站，用于通过回源拉流实现大规模分发）。

### Origin Server (Main) 配置
Origin server 接收来自编码器（OBS, FFmpeg 等）的 RTMP 推流，并将流分发给 edge 或直接提供给播放器。

最小化 `origin.conf` 示例（或修改 full.conf）：

```conf
listen              1935;           # RTMP listen port for publishers/players
max_connections     1000;
pid                 objs/origin.pid;
srs_log_file        ./objs/origin.log;

vhost __defaultVhost__ {
    # No special cluster config needed on origin
    # You can enable HLS/HTTP-FLV etc. here if needed
    hls {
        enabled         on;
        hls_path        ./objs/nginx/html;
        hls_fragment    10;
        hls_window      60;
    }
}
```

使用以下命令运行：
```
./objs/srs -c origin.conf
```

客户端推流至：`rtmp://your-origin-ip/live/stream_key`

### Edge Server 配置
当播放器连接时，Edge server 会向 origin **按需拉流**（on-demand），这种模式比 forward 模式更适合大规模扩展。

最小化 `edge.conf` 示例：

```conf
listen              1935;           # RTMP listen port for players (and sometimes publishers)
max_connections     5000;           # Edges usually handle more connections
pid                 objs/edge.pid;
srs_log_file        ./objs/edge.log;

vhost __defaultVhost__ {
    cluster {
        mode            remote;     # Most common mode: pull from origin on demand
        origin          192.168.1.10:1935;   # Change to your origin IP:port
        # Or multiple origins (SRS will try next one if current fails):
        # origin        192.168.1.10:1935 192.168.1.11:1935;
        
        # Optional: edge cluster name (for stats/management)
        # name          edge001;
        
        # Optional: only pull when there are players (default behavior)
    }
    
    # Optional: enable HTTP-FLV/HLS on edge too
    http_remux {
        enabled     on;
        mount       [vhost]/live/livestream.flv;
    }
}
```

使用以下命令运行：
```
./objs/srs -c edge.conf
```

播放器连接至：`rtmp://your-edge-ip/live/stream_key`  
如果流本地没有缓存，SRS edge 将自动从 origin 拉取。

### 关键差异总结

| Item              | Origin (Main) Server                  | Edge Server                              |
|-------------------|---------------------------------------|------------------------------------------|
| Role              | 接收编码器的 publish 推流               | 服务大量播放器，从 origin 拉流            |
| cluster.mode      | 未设置 (或根据需要设为 local)          | remote                                   |
| origin config     | 不需要                                | 必须设置：origin 的 IP:port               |
| Typical use       | 核心/中心服务器                         | CDN 边缘节点，多实例部署                  |
| Pull on demand    | 不适用                                | 是 (仅在有人播放时获取流)                 |

### 进阶说明
- 使用多个 origin server：`origin 1.2.3.4:1935 5.6.7.8:1935;`
- 对于超大规模场景 → 结合 SRS edge (处理 RTMP/HTTP-FLV) + NGINX 处理 HLS 缓存。
- 在最新的 SRS 版本 (v5/v6) 中，配置格式基本一致，但请始终参考 GitHub 上最新的 full.conf 示例以了解新特性。

**References:**

- [https://ossrs.net/lts/en-us/docs/v5/doc/edge](https://ossrs.net/lts/en-us/docs/v5/doc/edge)
- [https://ossrs.net/lts/en-us/docs/v5/doc/sample-rtmp-cluster](https://ossrs.net/lts/en-us/docs/v5/doc/sample-rtmp-cluster)
- [https://github.com/ossrs/srs/wiki/v2_EN_Edge](https://github.com/ossrs/srs/wiki/v2_EN_Edge)
- [https://github.com/ossrs/srs/blob/develop/trunk/conf/full.conf](https://github.com/ossrs/srs/blob/develop/trunk/conf/full.conf)