---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 解决Nextcloud-Talk配置错误
translated: true
type: note
---

问题：如何解决 OpenClaw 中关于遗留 Nextcloud-Talk 设置的 "invalid config" 错误？

回答：该错误提示配置键 `allowPrivateNetwork` 在 OpenClaw 2026.4.5 中已被弃用，并替换为更明确的安全设置。您可以通过手动更新 JSON 配置文件或使用内置修复工具来解决此问题。

### 选项一：自动修复（推荐）

让 OpenClaw CLI 处理迁移是修复语法的最快方式。请在终端中运行以下命令：

```bash
openclaw doctor --fix
```

这将自动在您的 `~/.openclaw/openclaw.json` 文件中将遗留键名更新为新标准。

### 选项二：手动编辑

如果您希望手动编辑文件，请打开 `/home/lzw/.openclaw/openclaw.json` 并找到 `nextcloud-talk` 通道部分。

**旧配置：**

```json
"nextcloud-talk": {
  "allowPrivateNetwork": true
}
```

**新配置：**

```json
"nextcloud-talk": {
  "network": {
    "dangerouslyAllowPrivateNetwork": true
  }
}
```

### 重启网关

保存更改后，您可以重启服务：

```bash
openclaw gateway restart
```
