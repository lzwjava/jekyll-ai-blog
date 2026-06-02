---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: Liberty 服务器命令指南
translated: true
type: note
---

**Question:** WebSphere Liberty server.sh / server.bat 命令行选项完整介绍

**Answer:**

WebSphere Liberty (也称为 WebSphere Application Server Liberty) 使用单一的 **server** 脚本/命令来执行大多数管理任务。

- 在 Unix/Linux 上 → `server.sh`
- 在 Windows 上 → `server.bat`

该脚本位于 `wlp/bin/` 目录（或 Open Liberty 的 `$OPEN_LIBERTY_HOME/bin/`）下。

通用语法为：

```bash
server <action> [serverName] [options]
```

如果未指定 `serverName`，则默认使用 **defaultServer**。

### 主要 Action (命令)

- **create** — 创建新的 server 目录和基础配置文件
  示例：`server create myServer`

- **start** — 在 **后台** 启动 server (最常用于生产环境)
  示例：`server start myServer`

- **run** — 在 **前台** 启动 server (控制台输出保留在当前终端；适用于开发/调试)
  示例：`server run myServer`

- **stop** — 正常停止 server
  示例：`server stop myServer`

- **status** — 检查 server 是否正在运行
  示例：`server status myServer`

- **package** — 将 server (包括配置和应用程序) 打包成 .zip, .jar, 或 .tar.gz 文件
  示例：`server package myServer --include=usr`

- **dump** — 创建诊断快照 (thread dump, configuration, trace 等)
  示例：`server dump myServer`

- **javadump** — 从运行中的 server 请求 Java core dump / heap dump
  示例：`server javadump myServer`

- **help** — 显示 server 命令或特定 action 的帮助信息
  示例：`server help start`

### 常用选项 (适用于 start/run/stop/package/dump 等)

| 选项                          | 描述                                                                        | 适用 Action         | 示例                                  |
|-------------------------------|-----------------------------------------------------------------------------|---------------------|--------------------------------------|
| `--clean`                     | 在启动前删除所有持久化的缓存数据 (OSGi resolver cache, transformed classes 等) | start, run          | `server start --clean`              |
| `--timeout=<seconds>`         | 等待 server 停止的最大时间 (秒) (默认 30–60s，取决于版本)                     | stop                | `server stop --timeout=120`         |
| `--timeout=2m30s`             | 支持单位：s, m, h (Open Liberty ~23.x 开始支持；WebSphere Liberty 后续版本)  | stop                | `server stop --timeout=3m`          |
| `--include={all,usr,bin}`     | 控制打包内容 (all = 完整 server + usr; usr = 仅配置/应用)                    | package             | `server package --include=usr`      |
| `--archive=filename.zip`      | 指定 package 命令的输出文件名                                                | package             | `server package --archive=my.zip`   |
| `--template=...`              | 在 create 时使用自定义 server 模板                                           | create              | `server create --template=javaEE7`  |
| `--osgiDebug`                 | 启用 OSGi 控制台 (用于调试 bundle 问题)                                      | start, run          | `server run --osgiDebug`            |
| `--debug[=<port>]`            | 启用 JVM 远程调试 (suspend=y,n; 默认端口 7777)                               | start, run          | `server start --debug=8888`         |
| `--json`                      | 以 JSON 格式输出 (适用于脚本处理)                                           | status, dump 等     | `server status --json`              |
| `--variable_name=value`       | 在启动时覆盖 server 变量 (需放在 `--` 之后)                                   | start, run          | `server start -- --http.port=9082`  |

### 关于变量覆盖的重要说明

若要在启动时传递 JVM 属性、Liberty 变量或系统属性：

```bash
server start myServer -- --my.custom.prop=value -Djavax.net.ssl.trustStore=...
```

在变量/属性覆盖之前必须使用 `--` 分隔符。

### 快速参考示例

```bash
# 创建新 server
server create testServer

# 后台启动并清理缓存
server start testServer --clean

# 前台启动并开启调试端口 7777
server run testServer --debug=7777

# 使用较长的超时时间停止 server
server stop testServer --timeout=180

# 创建轻量级可运行包 (仅包含 usr 文件夹内容)
server package testServer --include=usr --archive=testServer-usronly.zip

# 在运行时获取诊断 dump
server dump testServer
```

### 获取最新列表的途径

官方参考文档通常可在 IBM Docs 中找到：

"Server command options" → <https://www.ibm.com/docs/en/was-liberty/base?topic=reference-server-command-options>

对于 Open Liberty (语法非常相似，近年来通常完全一致)：
<https://openliberty.io/docs/latest/reference/command/server-commands.html>

在你安装的版本中运行 `server help` 或 `server help start`，可以查看该特定 Liberty 版本所支持的准确选项。

**References:**

- [Server command options - IBM](https://www.ibm.com/docs/SSAW57_liberty/com.ibm.websphere.wlp.nd.multiplatform.doc/ae/rwlp_command_server.html)
- [server commands :: Open Liberty Docs](https://openliberty.io/docs/latest/reference/command/server-commands.html)
- [server start command :: Open Liberty Docs](https://openliberty.io/docs/latest/reference/command/server-start.html)
