---
audio: false
generated: true
image: false
lang: zh
layout: post
model: anthropic/claude-4.5-sonnet
title: Nginx 命令行基础知识
translated: true
type: note
---

Nginx (读作 "engine-x") 主要通过 `nginx` 命令行可执行文件进行控制。以下是关于其命令行选项以及如何有效使用它们的详尽指南。

## Basic Command Syntax

```bash
nginx [-?hqTtVv] [-c file] [-g directives] [-p prefix] [-s signal]
```

## Core Command Options

**`-?` 或 `-h`** — 显示有关可用命令行选项的帮助信息。

**`-v`** — 仅显示 Nginx 版本号。

**`-V`** — 显示 Nginx 版本、编译器版本以及构建时使用的配置参数。这对于排查故障和了解编译了哪些 modules 非常有用。

**`-t`** — 在不启动 Nginx 的情况下测试配置文件语法。这将检查 `nginx.conf` 及其相关配置文件中的错误。在生产环境中 reload 或 restart Nginx 之前，务必运行此命令。

**`-T`** — 测试配置文件并将整个经过验证的配置转储到标准输出。这会显示最终解析后的配置，有助于调试 includes 并了解 Nginx 如何解释你的 config。

**`-q`** — 在配置测试期间抑制非错误消息。在只想查看错误的脚本中非常有用。

**`-p prefix`** — 设置 Nginx 前缀路径（默认通常为 `/usr/local/nginx` 或 `/etc/nginx`）。这会覆盖编译时的前缀，并确定 Nginx 查找配置文件和其他资源的路径。

**`-c file`** — 指定替代配置文件，而不是使用默认文件（通常为 `/etc/nginx/nginx.conf`）。这允许你维护多个配置或测试新配置。

**`-g directives`** — 从命令行设置全局配置指令。这些指令会覆盖配置文件中的设置。例如：`nginx -g "daemon off;"` 会在前台运行 Nginx。

**`-s signal`** — 向 Nginx master process 发送信号。这是控制正在运行的 Nginx 实例的主要方式。

## Signal Options (配合 `-s` 使用)

**`nginx -s stop`** — 快速关闭。立即终止所有 worker processes，而不等待当前请求完成。

**`nginx -s quit`** — 平滑关闭（Graceful shutdown）。在停止前等待 worker processes 完成当前请求的处理。

**`nginx -s reload`** — 重新加载配置文件。Nginx 会测试新配置，然后使用新配置平滑重启 worker processes，同时保持业务可用性。这是应用配置更改最常用的命令。

**`nginx -s reopen`** — 重新打开日志文件。在日志轮转（log rotation）时非常有用，通常在日志文件被移动或重命名后调用。

## Practical Usage Examples

**启动 Nginx：**
```bash
nginx
```

**在应用更改前测试配置：**
```bash
nginx -t
```

**修改后重新加载配置：**
```bash
nginx -s reload
```

**查看 Nginx 版本和编译的 modules：**
```bash
nginx -V
```

**使用自定义配置文件运行 Nginx：**
```bash
nginx -c /path/to/custom/nginx.conf
```

**在前台运行 Nginx（常用于 containers）：**
```bash
nginx -g 'daemon off;'
```

**平滑关闭：**
```bash
nginx -s quit
```

**查看完整解析后的配置：**
```bash
nginx -T
```

## Process Management Notes

Nginx 使用 master-worker 进程模型。master process 读取配置并管理 worker processes，而 workers 处理实际请求。当你通过 `nginx -s` 发送信号时，你是在与 master process 通信，由它协调各个 workers。

对于生产环境，典型的 workflow 是：修改配置文件 → 运行 `nginx -t` 进行验证 → 运行 `nginx -s reload` 在不宕机的情况下应用更改。

你也可以使用标准 Unix 信号（`kill` 命令）直接向 Nginx master process 发送信号，但推荐使用 `nginx -s`，因为它更具移植性且语义明确。