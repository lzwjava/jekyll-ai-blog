---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 禁用Hermes中的审批
translated: true
type: note
---

这是我找到的内容：

三种跳过审批的方式，从最简单到最持久：

1. **`/yolo` 斜杠命令**（最简单，按会话生效）  
   在 hermes 会话内直接输入 `/yolo`，即可切换 YOLO 模式的开启/关闭。所有危险命令在该会话中都会被自动批准。该设置不会持久化到配置中——重启 hermes 后即重置。

2. **`HERMES_YOLO_MODE=1` 环境变量**（按进程生效，无需编辑配置文件）  
   ```bash
   HERMES_YOLO_MODE=1 hermes
   ```
   在模块导入时即被固定（`tools/approval.py` 第 29 行）——即使通过提示注入也无法在会话中途更改。适合“在此 shell 中始终跳过”的场景。

3. **编辑 `~/.hermes/config.yaml`**（持久化，适用于所有会话）  
   ```yaml
   approvals:
     mode: off
   ```
   `tools/approval.py:825-837` 处的代码处理了 YAML 1.1 的一个特性：裸 `off` 会被解析为布尔值 `False`——它会正确地将该值规范化为字符串 `"off"`，因此 `mode: off` 和 `mode: "off"` 均可正常工作。

**你需要手动编辑 config.yaml 吗？** 不需要。`/yolo` 命令是最快的方式——在会话中输入一个按键即可。但它仅适用于当前会话。如果你希望永久启用而不编辑文件，则需要使用环境变量方式，或者在 shell 配置文件中添加 `export HERMES_YOLO_MODE=1`。

目前没有暴露 `hermes config set approvals.mode off` 这样的 CLI 子命令——`/config` 命令是只读的（显示当前配置）。虽然内部存在 `save_config_value()` 函数，并被 `/reasoning` 等命令使用，但并没有一个斜杠命令将其包装用于任意配置键。实际上，如果能有一个通用的 `/config set <key> <value>` 命令会是一个不错的补充。

**我的建议：** 只需在每个会话开始时输入 `/yolo`。这是一个命令，无需更改任何配置，状态栏会显示 `⚠ YOLO`，以便你知道它已激活。