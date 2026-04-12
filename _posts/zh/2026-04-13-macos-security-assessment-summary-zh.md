---
audio: false
generated: true
image: false
lang: zh
layout: post
title: macOS安全评估摘要
translated: true
type: note
---

以下是我对这台 macOS 机器的完整安全评估：

## 登录活动概览

**仅有一位用户登录：`lzwjava`**（加上系统 `root` 账户，这属于正常情况）。

| 时间 | 用户 | 终端 | 备注 |
|------|------|----------|-------|
| 4月12日周日 22:36（今晚） | lzwjava | ttys010 | 仍处于登录状态（本 AI 代理） |
| 4月12日周日 22:32（今晚） | lzwjava | ttys001 | 仍处于登录状态（终端） |
| 4月11日周六 22:31 | lzwjava | ttys009 | 仍处于登录状态 |
| 4月11日周六 05:55 | lzwjava | ttys007 | 仍处于登录状态 |
| 4月10日周五 21:45（启动时间） | lzwjava | console + 4 ttys | 仍处于登录状态 |

机器在**4月10日周五 21:41 重启**，这解释了为何许多会话显示“仍处于登录状态”——它们只是重启前会话的残留记录。最后一次 `root` 登录发生在关机前 1 分钟的控制台。日志中未发现任何可疑的远程（SSH）登录。

## 安全评估：低风险

**无明显入侵迹象**，但以下是发现的情况：

### 正常现象：
- 仅有一个用户账户（`lzwjava`）有实际登录记录——无未知用户
- 无失败登录尝试记录
- 无任何 SSH 登录尝试（若不使用 SSH 则为良好状态）
- 存在三个管理员账户：`root`、`macadmin`、`lzwjava`——`macadmin` 是标准的 macOS 管理员组账户
- 未发现 SSH authorized_keys 文件（不存在未授权的 SSH 密钥访问）
- 无定时任务（cron jobs）
- 所有运行进程均为可识别应用

### 值得关注的事项（不一定是问题）：
1. **代理/VPN 工具**：已安装 ClashX Pro、ShadowsocksX-NG 和 V2RayU。这些在中国常用于突破 GFW，但开放的监听端口理论上可能存在配置错误
2. **运行在 8081 端口的 nginx**：以用户 lzwjava 身份运行——请确认是否为有意设置
3. **运行在 6379 端口的 Redis**：仅绑定到 localhost，因此无法从外部访问
4. **运行在 5432 端口的 PostgreSQL**：仅绑定到 localhost，与 Redis 情况相同
5. **微信**在多个 localhost 端口监听——属于正常行为
6. **mihomo**（基于 clash 的代理）作为活跃进程运行（PID 92432）
7. **已安装 Multipass**（Canonical 虚拟机工具）和 **Docker** 守护进程助手

### 若您有所顾虑，建议采取以下措施：
1. 在本地终端运行 `sudo log show --predicate 'eventMessage contains "authentication"' --last 24h` 查看所有认证事件
2. 确认 8081 端口（nginx）是否为有意设置——如非必要，可通过 `brew services stop nginx` 停止
3. 确保防火墙已启用：`sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate`
4. 如有疑虑请修改密码：系统偏好设置 > 用户与群组