---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Gloo 后端连接被阻断
translated: true
type: note
---

现已全部清理。以下是情况说明：

Gloo 错误很明确：

```
failed to connect ... local=[192.168.1.36]:20614, remote=[192.168.1.28]:56711, error=Connection timed out
```

TCPStore 在端口 29500 上的 rendezvous 工作正常（worker→master）。但对于实际的 Gloo 数据传输，master 需要回连到 worker 的临时端口——而这被阻止了。Worker（192.168.1.28 / xiaoxin）的防火墙阻止了高端口上的入站连接，而且你没有 sudo 权限来开放它。

三个选项：

1. **打开 worker 上的防火墙** — 需要 sudo 或物理访问来运行 `sudo ufw allow from 192.168.1.36` 或 `sudo iptables -I INPUT -s 192.168.1.36 -j ACCEPT`

2. **单节点多进程** — 在两个 rank 都在 1.36 上运行（有 62GB RAM，足够运行两个 d8 的 CPU worker）：

   ```
   torchrun --nnodes=1 --nproc_per_node=2 --master_port=29500 ...
   ```

3. **使用 `GLOO_SOCKET_IFNAME` + 显式端口范围** — 在 worker 上设置 `GLOO_PORT_RANGE` 为一个已知范围，然后仅开放那些端口（仍需要 sudo）

选项 2 是最快的路径——需要我设置吗？1.36 机器有 62GB RAM，因此两个 d8 worker（每个约 80M 参数）应该没问题。它不会像真正的双节点那样快，但确实能运行。
