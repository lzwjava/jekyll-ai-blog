---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hermes模型CLI使用指南
translated: true
type: note
---

`hermes model` 仅支持交互模式——没有 `set` 子命令，也没有 `--global` 标志。它只接受认证/门户参数（如 `--portal-url`、`--no-browser` 等），然后直接进入选择器（`hermes_cli/main.py:9161-9201`）。

两种操作方式：

1. 运行选择器：

   ```
   hermes model
   ```

2. 通过 `config set` 以非交互方式设置（`hermes_cli/main.py:10108-10112`）：

   ```
   hermes config set model anthropic/claude-opus-4.7
   ```

解析器中没有任何 `--global` 开关——`hermes config set` 会写入单一用户配置（`hermes config path` 可查看路径）。如需按项目划分作用域，需通过环境变量或工作目录自行管理，而非通过 CLI 标志。
