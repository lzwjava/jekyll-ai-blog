---
audio: false
generated: true
image: false
lang: en
layout: post
title: Average Ping Latency Measurement
translated: false
type: note
---

Done. Changes:

- `get_ping_delay(host, count=10)` — now runs `ping -c 10` and parses the `round-trip min/avg/max/stddev` line, returns the avg (index [1])
- Timeout scaled to `count + 2` seconds to accommodate 10 pings
- Output now shows `avg X.X ms` to make it clear it's averaged over 10 pings
- Scan phase (is_host_up) still uses fast single-ping, `--delay` only runs 10 pings for confirmed live hosts

Example output:
```
192.168.1.1 is up  avg 19.9 ms
```