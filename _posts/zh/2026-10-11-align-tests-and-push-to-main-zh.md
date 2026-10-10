---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 对齐测试并推送到主分支
translated: true
type: note
---

已推送到 `origin/main` — 工作树干净。

## 提交

| 提交 | 内容 |
|---|---|
| `64d35e3` **test: align gpu and note plugin tests with refactored code** | 修复了阻止 pre-commit hooks 的现有测试失败 |
| `d6ae2db` **feat(linux): add screen-lock command for Ubuntu/GNOME idle lock control** | `ww/linux/screen_lock.py` (new), dispatch in `ww/linux/main.py`, help in `ww/main.py`, `completions/_ww` |

## 为了让钩子变绿而修复的问题

1. **我的 pyright 错误** — `_bad_time()` 现在标注为 `-> NoReturn`，因此 `secs` 在解析失败检查后缩小类型。

2. **17 个过时的 GPU 测试**（`tests/linux/test_gpu.py`） — 提交 `c0a079b` 重写了 `ww/linux/gpu.py`（移除了 `get_gpu_info`/`check_proxy_settings`），但未更新测试。已根据当前 API 重写：`detect_gpus`（DRM sysfs + lspci）、nvidia/nouveau/amd 内存辅助函数、温度、渲染器、`tool_available` 和 `run()` 冒烟测试。

3. **2 个过时的笔记插件测试**（`tests/plugins/test_note_plugin.py`） — 它们从 `~/.hermes/plugins`（依赖于机器，比仓库副本旧）导入插件，并断言已移除的 `create_note_from_content` 调用。现在它们导入仓库副本（`agent_plugin/hermes/plugins/`），并通过临时队列文件断言队列行为（`custom_title` / `directory` 附加信息）。

4. **队列污染清理** — 旧测试将垃圾 `"x"*300` 条目写入你的实际 `~/.config/ww/note_queue.json`；我已将其移除，重写后的测试不再触及实际队列（已验证：完整运行后条目数为 0）。

最终状态：**1805 个测试通过，68 个跳过**，所有钩子通过（根据 AGENTS 的 `SKIP=bandit`），ruff/pyright 干净。