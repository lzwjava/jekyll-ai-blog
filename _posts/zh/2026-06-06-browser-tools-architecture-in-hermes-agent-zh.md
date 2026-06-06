---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hermes Agent中的浏览器工具架构
translated: true
type: note
---

以下是 Hermes Agent 中浏览器工具的工作原理。代码位于：

    ~/.hermes/hermes-agent/tools/browser_tool.py  （约 3,863 行）

架构概述：

1. AGENT-BROWSER CLI（核心引擎）
   Python 代码不直接使用 Playwright/Puppeteer，而是通过子进程调用一个名为 `agent-browser` 的 npm 包——这是一个封装了 Playwright/Chromium 的 Rust CLI。每个浏览器操作都是一个子进程调用：

     agent-browser [--cdp <ws_url> | --session <name>] [--json] <command> [args...]

   命令包括：open、click、fill、scroll、snapshot、screenshot、eval、press、close 等。

2. 三种后端（自动检测）

   a) 本地无头 Chromium（默认，零成本）
      - 使用 `--session <name>` 标志
      - agent-browser 启动/管理本地 Chromium 守护进程
      - 需要执行：`npx agent-browser install`（下载 Chromium）

   b) 云服务提供商（Browserbase、Browser Use、Firecrawl）
      - 使用 `--cdp <websocket_url>` 标志连接到远程浏览器
      - 提供商位于 plugins/browser/<vendor>/provider.py
      - 自动检测顺序：Browser Use → Browserbase
      - 配置：config.yaml 中的 browser.cloud_provider

   c) Camofox（反检测本地浏览器）
      - 当设置了 CAMOFOX_URL 环境变量时，通过 REST API 路由
      - 从 tools/browser_camofox.py 导入

3. 会话管理
   - _get_session_info(task_id) 创建/重用会话
   - 每个 task_id 在 /tmp 下拥有自己的 socket 目录
   - 拥有者 PID 追踪用于孤儿清理
   - 空闲超时：守护进程在空闲一段时间后自动终止
   - AGENT_BROWSER_SOCKET_DIR 隔离并发会话

4. 元素引用（@e1、@e2 等）
   - `browser_snapshot` 调用 `agent-browser snapshot`，返回无障碍树（ariaSnapshot）——基于文本的 DOM 表示
   - 每个可交互元素获得一个引用 ID（@e1、@e2、……）
   - `browser_click(@e5)` → `agent-browser click @e5`
   - `browser_type(@e3, "text")` → `agent-browser fill @e3 "text"`

5. 执行流程（关键函数）
   _run_browser_command(task_id, command, args) 位于第 1875 行：
   - 通过 _find_agent_browser() 找到 agent-browser 二进制文件
   - 通过 _get_session_info() 获取/创建会话
   - 构建命令：[agent-browser, --cdp/--session, ..., --json, command, args]
   - 作为子进程运行，使用临时文件存储 stdout/stderr（避免守护进程继承文件描述符导致管道挂起）
   - 解析 JSON 输出，处理超时（默认 30 秒）
   - 如果引擎不匹配，回退到 Lightpanda→Chrome

6. 安全层
   - SSRF 保护：在云模式下阻止私有/内部 URL
   - 机密信息泄露：阻止包含 API 密钥/令牌的 URL
   - 网站策略：可配置的允许/阻止列表
   - 云元数据端点始终被阻止（169.254.169.254 等）
   - 重定向后检查：如果重定向落在被阻止的 URL 上，则导航离开

7. 混合路由
   - browser.auto_local_for_private_urls（默认为 true）
   - 云提供商处理公共 URL，本地 Chromium 处理 LAN/localhost
   - 以 _navigation_session_key(task_id, url) 为键

8. CDP 监管器
   - browser_supervisor.py 监控对话框（alert/confirm/prompt）
   - 附加到 CDP 端点，根据策略自动接受/拒绝
   - 配置：browser.dialog_policy、browser.dialog_timeout_s

整个项目约 4,000 行 Python 代码，用于协调一个管理 Chromium 实例（本地或远程）的 Rust CLI 二进制程序，具备会话隔离、安全防护和多后端回退机制。
