---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4-fast
title: 使用管理员权限监控网络活动
translated: true
type: note
---

### 使用管理员权限监控 HTTP 请求与 TCP 连接

假设您正在使用具备 root/管理员权限的 Linux/Unix 类系统（如 Ubuntu、CentOS），可以通过命令行工具以符合道德规范的方式进行网络活动监控，用于故障排查、安全审计或渗透测试。**重要提示：仅限在您拥有或已获得明确授权的系统上操作——未经授权的监控属于违法行为。** 本文将重点介绍轻量级且无需图形界面的命令行工具。

#### 1. **监控所有 TCP 连接**

   使用内置工具如 `ss`（现代版 `netstat` 替代品）或 `tcpdump` 进行实时抓包。这些工具可显示活动连接、端口及进程信息。

- **列出所有当前 TCP 连接（静态视图）：**

     ```
     sudo ss -tunap
     ```

  - `-t`: 仅显示 TCP
  - `-u`: 如需 UDP（但您要求 TCP）
  - `-n`: 数字格式端口（禁用 DNS 解析）
  - `-a`: 所有状态（已建立、监听等）
  - `-p`: 显示所属进程
     输出示例：

     ```
     tcp   ESTAB  0      0      192.168.1.10:80     10.0.0.5:54321    users:(("nginx",pid=1234,fd=5))
     ```

     仅查看监听端口：`sudo ss -tlnp`

- **使用 watch 进行实时监控：**

     ```
     watch -n 1 'sudo ss -tunap'
     ```

     每秒刷新一次

- **实时捕获 TCP 流量（数据包层级）：**
     若未安装 `tcpdump` 请先安装：
  - Debian/Ubuntu: `sudo apt update && sudo apt install tcpdump`
  - RHEL/CentOS: `sudo yum install tcpdump`

     ```
     sudo tcpdump -i any tcp -n -v
     ```

  - `-i any`: 所有网络接口
  - `-n`: 禁用名称解析
  - `-v`: 详细输出
     添加 `port 80 or port 443` 可过滤 HTTP/HTTPS：
     `sudo tcpdump -i any tcp port 80 or tcp port 443 -n -v -A`（`-A` 可查看 HTTP 头部 ASCII 载荷）

     保存至文件供后续分析：`sudo tcpdump -i any tcp -w capture.pcap`

#### 2. **监控 HTTP 请求日志**

   HTTP 日志取决于您使用的网页服务器（Apache、Nginx 等）。若未运行网页服务器，可通过网络抓包（如上所述）检查 HTTP 流量。服务器专用日志查看方式：

- **Apache (httpd)：**
     日志通常位于：
  - Ubuntu: `/var/log/apache2/access.log`
  - CentOS: `/var/log/httpd/access_log`

     ```
     sudo tail -f /var/log/apache2/access.log
     ```

  - 实时显示请求信息：IP、时间戳、方法（GET/POST）、URL、状态码
     示例日志行：`192.168.1.100 - - [08/Oct/2025:10:00:00 +0000] "GET /index.html HTTP/1.1" 200 1234`

     查看所有日志：`sudo grep "GET\|POST" /var/log/apache2/access.log | less`

- **Nginx：**
     日志位于 `/var/log/nginx/access.log`

     ```
     sudo tail -f /var/log/nginx/access.log
     ```

     格式与 Apache 类似

- **无网页服务器的情况（通用 HTTP 嗅探）：**
     使用带 `-A` 参数的 `tcpdump` 转储 HTTP 载荷，或安装 `ngrep` 进行正则匹配：

     ```
     sudo apt install ngrep  # 按需安装
     sudo ngrep -d any 'GET|POST|HTTP' -O http_capture.pcap
     ```

     此命令可过滤并记录 HTTP 方法

- **进阶方案：搭建透明代理实现完整日志记录**
     安装 Squid 代理：`sudo apt install squid`
     配置 `/etc/squid/squid.conf` 记录所有 HTTP 流量（添加 `access_log /var/log/squid/access.log squid`）
     通过 iptables 重定向流量：`sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 3128`
     随后跟踪 Squid 日志：`sudo tail -f /var/log/squid/access.log`

#### 渗透测试实用技巧

- **工具组合使用：** 将 `tcpdump` 输出管道至 `grep` 进行模式匹配，例如：`sudo tcpdump -i any tcp port 80 -A | grep "User-Agent"`
- **Wireshark 可视化分析：** 安装 Wireshark（`sudo apt install wireshark`）后以 root 权限运行，打开 `.pcap` 文件进行分析
- **安全加固：** 监控结束后若存在敏感日志，可使用 `sudo truncate -s 0 /var/log/access.log` 清空日志
- **跨平台说明：**
  - Windows（管理员权限）：使用 `netstat -anob` 查看 TCP，事件查看器查看日志
  - macOS：使用 `netstat -an` 和 `tcpdump`

此方案无需外部工具即可实现全面监控，建议先在虚拟机中测试。

[Linux ss 命令手册页](https://man7.org/linux/man-pages/man8/ss.8.html)
[Tcpdump 使用教程](https://www.tcpdump.org/manpages/tcpdump.1.html)
[Apache 访问日志格式](https://httpd.apache.org/docs/2.4/logs.html)
