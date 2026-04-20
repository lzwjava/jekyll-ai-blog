---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 升级Opencode CLI
translated: true
type: note
---

问题：如何升级 OpenCode CLI？

答案：

要升级 **OpenCode**，您可以直接在终端中使用其内置的升级命令。

### ✅ 升级到最新版本

```bash
opencode upgrade
```

这将自动将 OpenCode 更新到最新可用版本。（[OpenCode][1]）

---

### 🎯 升级到特定版本

如果您需要指定版本（例如回滚或测试）：

```bash
opencode upgrade v1.2.0
```

或根据版本风格省略 `v`：

```bash
opencode upgrade 1.2.0
```

---

### ⚙️ 可选：指定安装方式

如果您通过包管理器安装了 OpenCode 并希望明确指定方式：

```bash
opencode upgrade --method npm
```

支持的方式包括：`curl`、`npm`、`pnpm`、`bun`、`brew`。（[OpenCode][1]）

---

### 🧠 重要说明

* 默认情况下，OpenCode 在启动时也可能自动检查更新。
* 如果需要（例如在稳定环境中），可以在配置中禁用自动更新。
* 升级也可用于**降级**，只需传入一个旧版本号即可。

---

如果您愿意，请告诉我您是如何安装 OpenCode 的（npm / brew / curl），我可以为您提供最适合您安装方式的最安全升级路径。

[1]: https://opencode.ai/docs/cli/?utm_source=chatgpt.com "CLI | OpenCode"