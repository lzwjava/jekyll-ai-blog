---
audio: false
generated: true
image: false
lang: en
layout: post
model: x-ai/grok-4.1-fast
title: Configuring SRS Origin and Edge Servers
translated: false
type: note
---

**Question:** In SRS (Simple RTMP Server), how to configure the edge endpoint and main (origin) endpoint?

**Answer:**

In SRS (Simple RTMP Server), the **main endpoint** is typically called the **origin server**, and the **edge endpoint** is the **edge server** (used for scaling to many viewers via pull from origin).

### Origin Server (Main) Configuration
The origin server receives RTMP pushes from encoders (OBS, FFmpeg, etc.) and serves streams to edges or directly to players.

Example minimal `origin.conf` (or use full.conf and modify):

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

Run it with:
```
./objs/srs -c origin.conf
```

Clients push to: `rtmp://your-origin-ip/live/stream_key`

### Edge Server Configuration
The edge server pulls streams from the origin **on-demand** when a player connects (better than forward mode for large scale).

Example minimal `edge.conf`:

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

Run it with:
```
./objs/srs -c edge.conf
```

Players connect to: `rtmp://your-edge-ip/live/stream_key`
SRS edge will automatically pull from origin if the stream isn't cached locally.

### Summary of Key Differences

| Item              | Origin (Main) Server                  | Edge Server                              |
|-------------------|---------------------------------------|------------------------------------------|
| Role              | Receives publish from encoder         | Serves many players, pulls from origin   |
| cluster.mode      | Not set (or local if needed)          | remote                                   |
| origin config     | Not needed                            | Required: IP:port of origin              |
| Typical use       | Core/central server                   | CDN edge node, many instances            |
| Pull on demand    | N/A                                   | Yes (only fetches when someone plays)    |

### Advanced Notes
- Use multiple origin servers: `origin 1.2.3.4:1935 5.6.7.8:1935;`
- For very large scale → combine SRS edge (for RTMP/HTTP-FLV) + NGINX for HLS caching
- In recent SRS versions (v5/v6), the config format is almost the same, but always check the latest full.conf example on GitHub for new features.

**References:**

- [https://ossrs.net/lts/en-us/docs/v5/doc/edge](https://ossrs.net/lts/en-us/docs/v5/doc/edge)
- [https://ossrs.net/lts/en-us/docs/v5/doc/sample-rtmp-cluster](https://ossrs.net/lts/en-us/docs/v5/doc/sample-rtmp-cluster)
- [https://github.com/ossrs/srs/wiki/v2_EN_Edge](https://github.com/ossrs/srs/wiki/v2_EN_Edge)
- [https://github.com/ossrs/srs/blob/develop/trunk/conf/full.conf](https://github.com/ossrs/srs/blob/develop/trunk/conf/full.conf)
