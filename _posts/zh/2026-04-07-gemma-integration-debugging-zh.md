---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Gemma集成调试步骤
translated: true
type: note
---

## 根源问题总结

Gemma 在 OpenClaw 中无法运行是由三个层层递进的问题导致的：

### 1. llama-server 未运行
OpenClaw 配置引用了位于 `http://192.168.1.36:8081/v1` 的 `llama-server` 提供程序，但该端口并无进程监听。旧的 `~/llama.sh` 脚本启动的是运行在 8000 端口上的另一个模型。

### 2. Gemma 4 的思考模式
启动 llama-server 后，其 `--reasoning auto` 选项检测到 Gemma 4 的思考模板，并将输出拆分为 `reasoning_content`（包含实际文本）和 `content`（空）。而 OpenClaw 读取的是 `content` 字段，因此得到了空白响应。通过使用 `--reasoning off` 修复此问题。

### 3. llama-server 绑定地址 + proxychains 路由（真正的阻碍）
这是最棘手的问题。由两方面原因共同导致：

- llama-server 默认仅绑定到 `127.0.0.1`，因此即使在同一台机器上，`http://192.168.1.36:8081` 也无法访问。
- OpenClaw 网关在 `proxychains4` 下运行（通过位于 `127.0.0.1:7891` 的 mihomo/Clash 路由）。即使在配置中启用 `localnet 192.168.0.0/255.255.0.0`，连接仍然失败，因为目标端口并未在该接口上实际开放。

我们无法使用 `localnet 127.0.0.0/255.0.0.0` 来绕过回环地址，因为这会破坏 SOCKS5 代理本身（mihomo 监听在 `127.0.0.1:7891`）。

解决方案：以 `--host 0.0.0.0` 参数启动 llama-server，使其监听所有网络接口，保持 baseUrl 为 `http://192.168.1.36:8081/v1`，并让 proxychains 的 localnet 排除规则为 `192.168.x.x` 的流量绕过代理。

### 最终有效的命令

```bash
nohup /home/lzw/projects/llama.cpp/build/bin/llama-server \
  -m /home/lzw/projects/llama.cpp/models/gemma-4-26B-A4B-it-UD-IQ3_S.gguf \
  --port 8081 --host 0.0.0.0 -c 32768 --reasoning off \
  >> /home/lzw/llama-server.log 2>&1 &
```

### 在服务器上所做的更改

| 项目 | 更改内容 |
|------|--------|
| `/etc/proxychains4.conf` | 取消注释 `localnet 192.168.0.0/255.255.0.0` |
| `~/.openclaw/openclaw.json` | baseUrl 曾被临时改为 `127.0.0.1`，现已恢复为 `192.168.1.36` |
| openclaw-gateway | 通过 systemctl 重启服务 |

### 仍未持久化

llama-server 是使用 `nohup` 手动启动的。重启后不会保留。考虑更新 `~/llama.sh` 脚本或为其创建 systemd 用户服务。
