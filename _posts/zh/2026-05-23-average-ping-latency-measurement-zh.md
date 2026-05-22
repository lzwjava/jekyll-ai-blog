---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 平均Ping延迟测量
translated: true
type: note
---

完成。更改如下：

- `get_ping_delay(host, count=10)` — 现在运行 `ping -c 10` 并解析 `round-trip min/avg/max/stddev` 行，返回平均值（索引 [1]）
- 超时时间调整为 `count + 2` 秒以适应 10 次 ping
- 输出现在显示 `avg X.X ms` 以明确它是 10 次 ping 的平均值
- 扫描阶段（is_host_up）仍然使用快速单次 ping，`--delay` 仅对确认存活的主机运行 10 次 ping

示例输出：
```
192.168.1.1 is up  avg 19.9 ms
```