---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: Apache Bench 网站服务器测试指南
translated: true
type: note
---

### 什么是 Apache Bench (ab)？

Apache Bench (ab) 是 Apache HTTP 服务器附带的一个简单命令行工具，用于对 Web 服务器进行性能基准测试。它向指定 URL 发送一定数量的 HTTP 请求，并测量每秒请求数、每个请求耗时、传输速率和错误率等指标。它非常适合快速负载测试，但在复杂场景下功能有限（例如默认不支持 HTTPS 或高级脚本——此类需求可考虑使用 JMeter 等工具）。

### 安装方法

ab 工具随 Apache HTTP 服务器捆绑提供。安装方式如下：

- **Ubuntu/Debian (Linux 系统)**：
  ```
  sudo apt update
  sudo apt install apache2-utils
  ```

- **macOS (通过 Homebrew)**：
  ```
  brew install httpd
  ```

- **Windows 系统**：
  从官网下载 Apache HTTP 服务器，将其 `bin` 目录添加至系统 PATH 环境变量。

- **验证安装**：
  运行 `ab -V` 检查版本信息。

### 基础用法

核心命令语法为：
```
ab [选项] URL
```

- **URL 格式**：需为完整 HTTP 地址，例如 `http://example.com/`（若需测试 HTTPS，需使用 `openssl s_client` 等封装工具或改用 `wrk` 等工具）。

常用选项：
- `-n <请求数>`：执行请求总数（默认值：1）。建议测试时设置为 100–1000。
- `-c <并发数>`：单次并发请求数（默认值：1）。建议保持较低数值（如 10–50）避免压垮服务器。
- `-t <秒数>`：按持续时间执行测试而非固定请求数。
- `-k`：启用 HTTP Keep-Alive（连接复用）。
- `-H "头域: 值"`：添加自定义头部（如用于身份验证）。
- `-p <文件>`：从文件读取 POST 数据。
- `-T <内容类型>`：设置 POST 请求的内容类型。
- `-l`：接受可变文档长度（适用于动态内容）。

### 操作示例

1. **简单 GET 请求测试**：
   对本地服务器进行 100 次请求、10 个并发用户的测试：
   ```
   ab -n 100 -c 10 http://localhost:8080/
   ```
   输出示例：
   ```
   服务器软件：        Apache/2.4.41
   服务器主机名：      localhost
   服务器端口：        8080

   文档路径：          /
   文档长度：          1234 字节

   并发数：           10
   测试耗时：         1.234 秒
   完成请求：         100
   失败请求：         0
   每秒请求数：       81.03 [#/秒] (均值)
   每个请求耗时：     123.456 [毫秒] (均值)
   ```

2. **带 POST 数据的测试**（如表单提交）：
   创建包含提交数据的 `postdata.txt` 文件（例如 `key=value`）：
   ```
   ab -n 50 -c 5 -p postdata.txt -T application/x-www-form-urlencoded http://example.com/api/endpoint
   ```

3. **按持续时间测试**：
   ```
   ab -n 10000 -c 20 -t 30 http://example.com/  # 最多 1 万次请求或 30 秒
   ```

### 结果解读

- **每秒请求数**：数值越高代表吞吐量越好
- **每个请求耗时**：数值越低代表延迟越优
- **传输速率**：带宽使用效率
- 关注“失败请求”或“非 2xx 响应”以发现问题
- 建议多次测试取平均值，因为缓存/网络波动可能导致单次结果偏差

### 技巧与限制

- **在独立机器运行**：尽量避免对本机测试以模拟真实流量
- **预热准备**：先发送少量请求激活缓存
- **扩展测试**：高负载场景建议使用 `wrk`、`siege` 或 Locust 等工具
- **HTTPS 支持**：ab 原生不支持 HTTPS，可通过代理或替代工具实现
- **错误处理**：若出现“socket: 打开文件过多”错误，需提高系统文件描述符限制（例如 `ulimit -n 4096`）

更多细节请查阅手册页（`man ab`）或官方文档。

[Apache Bench 官方文档](https://httpd.apache.org/docs/2.4/programs/ab.html)
