---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 赫尔墨斯插件系统架构详解
translated: true
type: note
---

以下是 Hermes 插件系统的工作原理：

## 架构概览

插件系统实现在 `hermes_cli/plugins.py`（约 1600 行）中。它包含三个核心类：

```
PluginManifest   →  解析后的 plugin.yaml 元数据
LoadedPlugin     →  运行时状态（模块、工具、钩子、命令）
PluginManager    →  单例，负责发现、加载、调用插件
PluginContext    →  提供给每个插件 register() 函数的门面（facade）
```

## 插件来源（4 条发现路径）

```
1. 内置    → plugins/<name>/           （随 hermes-agent 发布）
2. 用户    → ~/.hermes/plugins/<name>/ （用户安装）
3. 项目    → ./.hermes/plugins/<name>/ （通过 HERMES_ENABLE_PROJECT_PLUGINS 选择启用）
4. Pip    → entry_points 组 "hermes_agent.plugins"
```

后来源在名称冲突时覆盖前来源（用户 > 内置，项目 > 用户）。

## 插件结构

每个插件需要两个文件：

```
my-plugin/
├── plugin.yaml      # 清单（名称、版本、描述、类型、钩子）
└── __init__.py      # 必须包含 register(ctx) 函数
```

**plugin.yaml** 示例（`plugins/disk-cleanup/plugin.yaml`）：

```yaml
name: disk-cleanup
version: 2.0.0
description: "自动跟踪并清理临时文件"
hooks:
  - post_tool_call
  - on_session_end
```

****init**.py** 必须定义 `register(ctx)`：

```python
def register(ctx) -> None:
    ctx.register_hook("post_tool_call", _on_post_tool_call)
    ctx.register_hook("on_session_end", _on_session_end)
    ctx.register_command("disk-cleanup", handler=_handle_slash, description="...")
```

## 插件类型

```
standalone        → 默认，通过 plugins.enabled 选择启用
backend           → 现有工具的可插拔后端（image_gen, web, browser）
exclusive         → 只有一个活跃提供者的类别（memory）
platform          → 网关消息适配器（IRC, Teams 等）
model-provider    → 推理后端（openrouter, xai 等）
```

内置的 `backend` 和 `platform` 插件自动加载。其他所有插件均为选择启用。

## 插件可以注册的内容

通过 `PluginContext`：

```
ctx.register_tool(name, toolset, schema, handler)     → 全局工具注册表
ctx.register_hook(hook_name, callback)                 → 生命周期钩子
ctx.register_command(name, handler)                    → 斜杠命令（/foo）
ctx.register_cli_command(name, setup_fn, handler_fn)   → hermes <subcommand>
ctx.register_platform(name, label, adapter_factory)    → 网关适配器
ctx.register_context_engine(engine)                    → 替换上下文压缩器
ctx.register_image_gen_provider(provider)              → 图像生成后端
ctx.register_video_gen_provider(provider)              → 视频生成后端
ctx.register_web_search_provider(provider)             → 网页搜索后端
ctx.register_browser_provider(provider)                → 云浏览器后端
ctx.register_skill(name, path)                         → 插件作用域内的技能
ctx.inject_message(content, role)                      → 注入到对话中
ctx.dispatch_tool(tool_name, args)                     → 调用其他工具
ctx.llm                                                → 宿主拥有的 LLM 门面
```

## 生命周期钩子

```
pre_tool_call, post_tool_call
pre_llm_call, post_llm_call
pre_api_request, post_api_request
on_session_start, on_session_end, on_session_finalize, on_session_reset
transform_terminal_output, transform_tool_result, transform_llm_output
pre_gateway_dispatch
pre_approval_request, post_approval_response
subagent_stop
```

代理在适当位置调用 `invoke_hook(name, **kwargs)`。每个回调都被 try/except 包裹，因此损坏的插件不会使核心循环崩溃。

## 加载流程

```
discover_and_load()
  → 扫描 4 个来源以获取 plugin.yaml 清单
  → 按键去重（后来源胜出）
  → 跳过已禁用/exclusive/model-provider 类型
  → 对每个启用的插件：
      → 将 __init__.py 作为 hermes_plugins.<slug> 导入
      → 调用 register(ctx)
      → 跟踪已注册的工具/钩子/命令
```

## 关键文件

- `hermes_cli/plugins.py` — PluginManager、PluginContext、发现/加载
- `agent/plugin_llm.py` — PluginLlm 门面（宿主拥有的 LLM 访问）
- `plugins/` — 内置插件目录
- `~/.hermes/plugins/` — 用户插件目录
