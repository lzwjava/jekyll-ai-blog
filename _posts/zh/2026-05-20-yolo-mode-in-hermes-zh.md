---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 爱马仕中的Yolo模式
translated: true
type: note
---

以下是 Hermes 中变更内容的完整说明以及 yolo 模式的工作原理。

---

## 变更内容

在 `/home/xiaoxin/.hermes/config.yaml` 文件中，第 406-407 行：

```yaml
approvals:
  mode: false   # ← 之前未设置（默认为 'manual'）
```

该配置位于 `approvals` 部分（第 406-412 行），其中还包含 `timeout`、`cron_mode`、`mcp_reload_confirm` 和 `destructive_slash_confirm`。

---

## 作用说明

Hermes 拥有一个 **命令审批系统**，该系统会拦截可能具有破坏性的 shell 命令（如 `rm -rf`、`git reset --hard`、`chmod -R 777` 等），并在执行前要求您确认。该系统共有三种模式：

| 模式 | 行为 |
|------|------|
| `manual` | 始终在标记的命令执行前提示确认（默认） |
| `smart` | 使用小型 LLM 自动批准低风险命令，高风险命令则提示确认 |
| `off` / `false` | 跳过所有审批提示 — 这就是 **yolo 模式** |

将 `mode: false`（等同于 `off`）设置为 true 后，Hermes 将 **不再要求确认** 任何它认为危险的 shell 命令，而是直接执行。

---

## yolo 模式的适用范围

Yolo 模式仅影响 **危险命令的审批提示**。它不会改变以下内容：

- **机密信息脱敏**（`security.redact_secrets`）— 该功能独立运行
- **Tirith 安全策略**（`security.tirith_enabled`）— 安全规则仍然有效
- **工具访问权限** — 您的所有工具仍按之前的方式正常工作
- **任何其他配置** — 这是一个范围狭窄的开关

---

## 如何使用

| 方法 | 范围 |
|--------|-------|
| `hermes config set approvals.mode off` | **持久化** — 您刚刚已执行此操作 |
| `hermes --yolo` | 单次调用标志（一个会话） |
| `export HERMES_YOLO_MODE=1` | 针对当前 shell 的环境变量 |
| `/yolo`（会话内的斜杠命令） | 在当前会话中开启/关闭 |

---

## 生效时机

此类配置更改在会话启动时读取。对于 **未来的会话**（下次运行 `hermes` 时），yolo 模式将自动启用。如需在当前的会话中立即生效，请输入 `/yolo`（该命令会内联切换审批绕过功能）。

如需在之后恢复原设置：

```bash
hermes config set approvals.mode manual    # 恢复为默认提示
hermes config set approvals.mode smart     # 使用 AI 辅助审批
```
