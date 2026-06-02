---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 更新OpenClaw版本
translated: true
type: note
---

问题：如何将 OpenClaw 从 v2026.4.27 更新到 v2026.4.29？

回答：

更新其实非常简单——OpenClaw 内置了相关命令。

### ✅ 推荐方法（一条命令）

只需在终端中运行：

```bash
openclaw update
```

该命令将：

* 检测您的 OpenClaw 安装方式（npm 或 git）
* 下载最新版本（例如 v2026.4.29）
* 运行诊断（`doctor`）
* 自动重启网关（[OpenClaw][1]）

---

### 🔍 可选实用命令

如果您需要更多控制：

* 预览更新（安全检查）：

```bash
openclaw update --dry-run
```

* 切换到 beta/dev 频道：

```bash
openclaw update --channel beta
```

* 检查更新状态：

```bash
openclaw update status
```

---

### 🧪 更新后（重要步骤）

有时需要验证以确保更新完全生效：

```bash
openclaw doctor
openclaw gateway restart
openclaw health
```

这些步骤可确保您的系统运行干净且正常（[OpenClaw][1]）

---

### ⚠️ 如果 `openclaw update` 无效

#### 情况一：通过 npm/pnpm 全局安装

使用：

```bash
npm install -g openclaw@latest
# 或
pnpm add -g openclaw@latest
```

#### 情况二：通过脚本安装

重新运行安装程序：

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

该命令会自动就地升级（[OpenClaw][2]）

---

### ⚠️ 实际注意事项（重要）

近期版本（4.x 系列）有时会引入重大变更。例如：

* 环境变量重命名
* 配置路径变更（`~/.moltbot` → `~/.openclaw`）

如果您的配置经过自定义修改，请谨慎更新（或先使用 `--dry-run` 测试）。

---

### 💡 快速总结

* 最快方式：`openclaw update`
* 若遇问题：通过 npm 或脚本重新安装
* 更新后务必运行 `doctor`

---

如果您需要，请告诉我 OpenClaw 的安装方式（npm / docker / 源码），我可以为您提供**针对您具体设置的精确升级路径**。

[1]: https://docs.openclaw.ai/install/updating?utm_source=chatgpt.com "更新 - OpenClaw"
[2]: https://docs.openclaw.ai/updating?utm_source=chatgpt.com "更新 - OpenClaw"
