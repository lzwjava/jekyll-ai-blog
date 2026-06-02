---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 赫尔墨斯代理架构概述
translated: true
type: note
---

基于对代码库的探索，以下是 Hermes Agent 的架构：

HERMES AGENT 架构
=================

1. 核心入口点
------------
- run_agent.py（AIAgent 类）——核心对话循环，约 12k 行代码
- cli.py（HermesCLI 类）——交互式 CLI 编排器，约 11k 行代码
- model_tools.py——工具编排、发现与调度

2. 主要组件
-----------

AIAgent（run_agent.py）
  - 主代理循环：用户消息 → LLM 调用 → 工具调用 → 重复
  - 处理：模型提供商、消息历史、预算跟踪、中断
  - 支持多种 API 模式：chat_completions、codex_responses 等
  - 默认最多 90 次工具调用迭代

工具系统（tools/ + model_tools.py）
  - tools/registry.py——中央注册表，自动发现 tools/*.py
  - 每个工具文件在导入时调用 registry.register()
  - 工具按“工具集”组织（web、terminal、file 等）
  - 处理程序必须返回 JSON 字符串

CLI（cli.py）
  - 使用 Rich 实现横幅/面板，prompt_toolkit 处理输入
  - 皮肤引擎支持主题（default、ares、mono、slate）
  - hermes_cli/commands.py 中的斜杠命令注册表
  - 命令：/help、/model、/skin、/note 等

网关（gateway/）
  - 消息平台：telegram、discord、slack、whatsapp、signal、matrix 等
  - gateway/platforms/ 中的平台适配器
  - 通过 SQLite 进行会话管理（hermes_state.py）
  - 运行方式：hermes gateway

3. 插件系统（plugins/）
-----------------------
- PluginManager 从 ~/.hermes/plugins/、./.hermes/plugins/、pip 发现插件
- 插件可以注册：
  - 工具（ctx.register_tool）
  - 命令（ctx.register_command）
  - 钩子（工具/LLM 调用前后）
  - 模型提供商
  - 记忆提供商
  - 图像/视频生成提供商

4. 配置与状态
--------------
- ~/.hermes/config.yaml——设置
- ~/.hermes/.env——仅 API 密钥
- ~/.hermes/skills/——自定义技能
- ~/.hermes/plugins/——自定义插件
- ~/.hermes/skins/——自定义主题
- 日志：~/.hermes/logs/（agent.log、errors.log）

5. 依赖流程
----------
tools/registry.py（无依赖）
       ↑
tools/*.py（在模块级别导入 registry）
       ↑
model_tools.py（导入 registry 并触发发现）
       ↑
run_agent.py、cli.py、batch_runner.py

6. 技能系统
-----------
- skills/ 目录中的内置技能
- optional-skills/ 中的可选技能
- ~/.hermes/skills/ 中的自定义技能
- 作为用户消息（而非系统提示）加载以实现提示缓存
- 每个技能是一个包含 YAML 前置元数据的 SKILL.md 文件

7. 附加组件
-----------
- ui-tui/——Ink (React) 终端 UI
- tui_gateway/——TUI 的 Python JSON-RPC 后端
- acp_adapter/——ACP 服务器（VS Code/Zed/JetBrains）
- cron/——任务调度器
- batch_runner.py——并行批处理
- website/——Docusaurus 文档

该架构遵循干净的基于插件的设计，其中：
- 核心代理循环简单：LLM → 工具 → 重复
- 工具被自动发现并注册
- 平台通过网关适配器可插拔
- 所有内容均可通过插件扩展
