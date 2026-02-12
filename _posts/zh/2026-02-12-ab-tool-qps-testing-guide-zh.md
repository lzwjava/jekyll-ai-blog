---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: QPS 测试 AB 工具指南
translated: true
type: note
---

问题：请全面介绍 AB 性能测试、AB 命令、AB 工具以及如何测试 QPS。

回答：

**ApacheBench (ab)** 是一个简单、轻量级的命令行基准测试和 Load Testing 工具，包含在 **Apache HTTP Server** 发行版中。它旨在通过发送大量请求并报告关键指标来衡量 HTTP/HTTPS 服务器的 **Performance**。

尽管 **ab** 最初是为测试 Apache 开发的，但它对 **任何 HTTP Server**（如 Nginx、Node.js/Express、Go、Java Spring、Python Flask/FastAPI 等）都表现良好。

### ab 的主要用途
- 快速估算服务器每秒可以处理多少请求（**QPS / RPS**）
- 衡量不同 Concurrency（并发）级别下的 **Response Latency**（响应延迟）
- 识别单个 Endpoint（端点）的大致 **Breaking Points**（崩溃点）或饱和点
- 比较代码或 Configuration 更改前后的性能

**ab 并不是**一个功能完备的 Load Testing 工具（相比于 JMeter、Locust、k6、Gatling、wrk 等）。它有一定的局限性：
- 仅支持 **HTTP/1.0 和 HTTP/1.1**（不支持 HTTP/2 或 HTTP/3）
- 无法进行高级 Scripting 或复杂场景模拟
- 仅支持单机测试（无 Distributed Testing）
- 对 Request Body 的支持非常简单

尽管如此，它在快速 Smoke Tests（冒烟测试）、CI/CD Pipeline 检查和基础 QPS 验证中仍然非常受欢迎。

### 如何安装 ab
大多数 Linux 发行版将其包含在 `apache2-utils` 或 `httpd-tools` 软件包中。

```bash
# Ubuntu / Debian
sudo apt update
sudo apt install apache2-utils

# CentOS / Rocky / AlmaLinux
sudo dnf install httpd-tools    # 或 yum install httpd-tools

# macOS (通过 Homebrew)
brew install httpd

# Windows: 通常通过 XAMPP / WAMP 安装，或从 Apache bin 目录中复制 ab.exe
```

检查版本：
```bash
ab -V
# ApacheBench, Version 2.3 <$Revision: ... $>
```

### 基础用法与 QPS 测试的核心参数
```bash
ab [options] [http[s]://]hostname[:port]/path
```

QPS 测试中最重要的选项：

| 选项 | 含义 | QPS 测试的典型用法 |
|--------------|--------------------------------------|---------------------------------------------|
| `-n NUMBER` | 要发送的总请求数 | `-n 1000` 或 `-n 5000` 或 `-n 20000` |
| `-c NUMBER` | Concurrency（并发连接数） | `-c 10`, `-c 50`, `-c 200`, `-c 500` ... |
| `-k` | 使用 HTTP Keep-Alive（非常重要！） | 几乎总是使用 `-k` |
| `-t SECONDS` | 最大基准测试时间（代替 -n） | `-t 30`（运行 30 秒） |
| `-s SECONDS` | 每个请求的 Socket 超时时间 | `-s 10`（默认为 30） |
| `-p FILE` | POST 数据文件 | 用于 POST/PUT 请求 |
| `-T type` | POST 数据的 Content-Type | `-T application/json` |
| `-C cookie` | 添加 Cookie Header | `-C "session=abc123"` |
| `-H header` | 自定义 Header | `-H "Authorization: Bearer xyz"` |
| `-g FILE` | 输出 gnuplot 兼容数据 | 用于后续绘图 |

### 经典的 QPS 测试模式

1. **快速冒烟测试**（小负载）
```bash
ab -n 1000 -c 20 -k https://your-api.com/health
```

2. **典型的真实 API 测试**
```bash
ab -n 5000 -c 100 -k \
   -H "Authorization: Bearer eyJhb..." \
   https://api.example.com/v1/users/profile
```

3. **POST JSON 测试**
```bash
# 准备 postdata.json
echo '{"username":"test","password":"123456"}' > postdata.json

ab -n 2000 -c 50 -k \
   -p postdata.json -T application/json \
   https://api.example.com/login
```

4. **寻找近似最大 QPS**
通过逐渐增加并发数运行多次测试：

```bash
ab -n 10000 -c  50 -k https://...
ab -n 10000 -c 100 -k https://...
ab -n 10000 -c 200 -k https://...
ab -n 10000 -c 400 -k https://...
# ... 直到吞吐量停止增长或出现错误
```

### 理解最重要的输出行

```
Server Software:        nginx/1.24.0
Server Hostname:        example.com
Server Port:            443
SSL/TLS Protocol:       TLSv1.3,TLS_AES_256_GCM_SHA384,...

Document Path:          /api/products
Document Length:        1245 bytes

Concurrency Level:      100
Time taken for tests:   12.348 seconds
Complete requests:      10000
Failed requests:        0
Total transferred:      13250000 bytes
HTML transferred:       12450000 bytes

**Requests per second:  809.85 [#/sec] (mean)**     ← 这就是 QPS!
**Time per request:     123.456 [ms] (mean)**       ← 平均延迟
**Time per request:     1.235 [ms] (mean, across all concurrent requests)**
Transfer rate:          1048.12 [Kbytes/sec] received

Percentage of the requests served within a certain time (ms)
  50%    118
  66%    125
  75%    132
  80%    138
  90%    156
  95%    189
  98%    245
  99%    312
 100%    456 (longest request)
```

需要关注的关键指标：
- **Requests per second (mean)** → 主要的 QPS 数值
- **Time per request (mean)** → 客户端看到的平均延迟
- **Failed requests** → 应为 0（或非常低）
- **90%/95%/99% latency** → 尾部延迟（Tail Latency，对用户体验非常重要）
- 当增加 `-c` 但 **QPS 停止显著增长**时 → 达到饱和点

### 建议与最佳实践
- 为进行真实的 HTTP/1.1 测试，务必使用 `-k` (Keep-Alive)
- 运行多次测试并取中位数/平均值（避免异常值）
- 从网络状况良好的机器对目标进行测试（低延迟）
- 逐渐增加并发，直到出现错误或延迟飙升
- 比较优化前后的同项测试结果
- 对于严肃的生产环境测试 → 考虑使用 wrk, k6, Locust, 或 Gatling

**ab** 仍然是获取任何 HTTP Endpoint 大致但有用的 QPS/Latency 概况的最快方法之一。

参考资料：

- [Official ApacheBench documentation](https://httpd.apache.org/docs/2.4/programs/ab.html)
- [Datadog guide on using ApacheBench](https://www.datadoghq.com/blog/apachebench)
- [Baeldung tutorial on load testing with ab](https://www.baeldung.com/linux/ab-apachebench-load-testing)