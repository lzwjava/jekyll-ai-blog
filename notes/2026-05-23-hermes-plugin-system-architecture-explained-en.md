---
audio: false
generated: true
image: false
lang: en
layout: post
title: Hermes Plugin System Architecture Explained
translated: false
type: note
---

Here's how the Hermes plugin system works:

## Architecture Overview

The plugin system is implemented in `hermes_cli/plugins.py` (~1600 lines). It has three core classes:

```
PluginManifest   →  parsed plugin.yaml metadata
LoadedPlugin     →  runtime state (module, tools, hooks, commands)
PluginManager    →  singleton that discovers, loads, invokes plugins
PluginContext    →  facade handed to each plugin's register() function
```

## Plugin Sources (4 discovery paths)

```
1. Bundled   → plugins/<name>/           (shipped with hermes-agent)
2. User      → ~/.hermes/plugins/<name>/ (user-installed)
3. Project   → ./.hermes/plugins/<name>/ (opt-in via HERMES_ENABLE_PROJECT_PLUGINS)
4. Pip       → entry_points group "hermes_agent.plugins"
```

Later sources override earlier ones on name collision (user > bundled, project > user).

## Plugin Structure

Each plugin needs two files:

```
my-plugin/
├── plugin.yaml      # manifest (name, version, description, kind, hooks)
└── __init__.py      # must have register(ctx) function
```

**plugin.yaml** example (`plugins/disk-cleanup/plugin.yaml`):
```yaml
name: disk-cleanup
version: 2.0.0
description: "Auto-track and clean up ephemeral files"
hooks:
  - post_tool_call
  - on_session_end
```

**__init__.py** must define `register(ctx)`:
```python
def register(ctx) -> None:
    ctx.register_hook("post_tool_call", _on_post_tool_call)
    ctx.register_hook("on_session_end", _on_session_end)
    ctx.register_command("disk-cleanup", handler=_handle_slash, description="...")
```

## Plugin Kinds

```
standalone      → default, opt-in via plugins.enabled
backend         → pluggable backend for existing tools (image_gen, web, browser)
exclusive       → category with one active provider (memory)
platform        → gateway messaging adapters (IRC, Teams, etc.)
model-provider  → inference backends (openrouter, xai, etc.)
```

Bundled `backend` and `platform` plugins auto-load. Everything else is opt-in.

## What Plugins Can Register

Via `PluginContext`:

```
ctx.register_tool(name, toolset, schema, handler)     → global tool registry
ctx.register_hook(hook_name, callback)                 → lifecycle hooks
ctx.register_command(name, handler)                    → slash commands (/foo)
ctx.register_cli_command(name, setup_fn, handler_fn)   → hermes <subcommand>
ctx.register_platform(name, label, adapter_factory)    → gateway adapters
ctx.register_context_engine(engine)                    → replace context compressor
ctx.register_image_gen_provider(provider)              → image gen backends
ctx.register_video_gen_provider(provider)              → video gen backends
ctx.register_web_search_provider(provider)             → web search backends
ctx.register_browser_provider(provider)                → cloud browser backends
ctx.register_skill(name, path)                         → plugin-scoped skills
ctx.inject_message(content, role)                      → inject into conversation
ctx.dispatch_tool(tool_name, args)                     → call other tools
ctx.llm                                                → host-owned LLM facade
```

## Lifecycle Hooks

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

The agent calls `invoke_hook(name, **kwargs)` at the right points. Each callback is wrapped in try/except so a broken plugin can't crash the core loop.

## Loading Flow

```
discover_and_load()
  → scan 4 sources for plugin.yaml manifests
  → deduplicate by key (later sources win)
  → skip disabled/exclusive/model-provider
  → for each enabled plugin:
      → import __init__.py as hermes_plugins.<slug>
      → call register(ctx)
      → track registered tools/hooks/commands
```

## Key Files

- `hermes_cli/plugins.py` — PluginManager, PluginContext, discovery/loading
- `agent/plugin_llm.py` — PluginLlm facade (host-owned LLM access)
- `plugins/` — bundled plugins directory
- `~/.hermes/plugins/` — user plugins directory
