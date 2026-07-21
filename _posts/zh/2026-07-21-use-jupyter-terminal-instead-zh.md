---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用Jupyter终端
translated: true
type: note
---

端口 31154 正在容器内部 **监听**（这是我们启动的 SSH 守护进程）。但云代理可能没有在外部转发流量到该端口。

**要检查 SSH 是否真的可以从外部访问，请在容器内运行以下命令：**

```bash
# 1. Check if SSH is listening on the right interface
cat /proc/net/tcp | grep "$(printf '%04X' 31154 | sed 's/\\(..\\)\\(..\\)/\2\1/')"

# 2. Check what external IP the container sees
curl -s ifconfig.me 2>/dev/null || echo "no external IP"

# 3. Test SSH locally (from inside the container to itself)
ssh -o StrictHostKeyChecking=no -o ConnectTimeout=5 root@localhost -p 31154 "echo SSH_LOCAL_OK"
```

**要从你的 Mac（外部）测试：**

```bash
ssh -o ProxyCommand=none -v root@36.150.116.206 -p 31154 2>&1 | head -10
```

但根据我之前从我这边的测试，**外部端口 31154 仍然被拒绝**——云代理在崩溃后没有重新映射它。

**最简单的做法**：直接使用 Jupyter 终端运行 FLUX.1-dev，无需 SSH。
