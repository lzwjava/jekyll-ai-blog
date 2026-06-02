---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hermes笔记插件无需修改源代码
translated: true
type: note
---

Clean — 无源文件更改。以下是总结：

---

**你说得对——插件方式才是正确的做法。** 我已撤销源文件的更改。以下是构建的内容：

**创建的文件（未修改源文件）：**

```
~/.hermes/plugins/note/
├── plugin.yaml          # 清单文件
└── __init__.py          # 通过 ctx.register_command() 注册 /note 命令
```

**配置更改：**

```
~/.hermes/config.yaml — 在 plugins.enabled 中添加了 "note"
```

**工作原理：**

该插件使用官方的 `ctx.register_command()` API（详见 `hermes_cli/plugins.py` 第 412 行）。它会：

1. 从 `ctx._manager._cli_ref`（CLI 实例）获取对话历史
2. 提取最后一条助手回复（支持字符串或 OpenAI 多部分内容）
3. 去除推理标签（`
