---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 禁用Hermes代理批准提示
translated: true
type: note
---

**问题：** 在 Hermes Agent 中，它经常标记危险命令并要求逐一批准——如何允许任何命令而无需每次都提示？

**回答：**

Hermes Agent（由 NousResearch 开发）具有多层安全系统用于命令批准。以下是减少或绕过批准提示的所有方法的全面说明，并附有适当警告。

---

## 了解批准系统

在执行任何命令之前，Hermes 会将其与精心策划的危险模式列表进行比对。如果匹配，用户必须明确批准。批准系统支持三种模式，通过 `~/.hermes/config.yaml` 中的 `approvals.mode` 配置。

```yaml
approvals:
  mode: manual   # manual | smart | off
  timeout: 60    # 自动拒绝前的等待秒数
```

---

## 选项 1：禁用所有批准提示 (`approvals.mode: off`)

这是最直接的方法。将 `approvals.mode` 设置为 `off` 会禁用所有安全提示。

```yaml
# ~/.hermes/config.yaml
approvals:
  mode: off
```

> ⚠️ **警告：** 警告：** 这意味着 Hermes 将运行任何终端命令而无需事先询问你（绝对阻止列表除外——见下文）。

---

## 选项 2：使用 "Smart" 模式（LLM 风险评估）

除了 `off`off` 之外，你可以将模式设置为 `smart`：

使用辅助 LLM 评估风险。安全命令将自动通过；只有真正有风险的命令才会提示你。

```yaml
approvals:
  mode: smart
```

这是一种折中方案——更少的干扰，但并非完全盲目。

---

## 选项 3：使用 Docker/容器后端（出于安全考虑推荐）

对于生产环境网关部署，使用 `docker`、`modal`、`daytona` 或 `vercel_sandbox` 后端来隔离代理命令与主机系统。这完全消除了危险命令批准的需要。

```yaml
terminal:
  backend: docker
  docker_image: "nikolaik/python-nodejs:python3.11-nodejs20"
  container_persistent: true
```

当在容器内运行时，危险命令检查会被跳过，因为容器已经提供了隔离。这是允许所有命令的**最安全**方式——命令在沙箱内自由运行，而不是在你的主机上。

---

## 选项 4：使用 `--yolo` 标志（仅 CLI）

`--yolo` 标志在代码库中被引用为一种在 CLI 中跳过批准层的方式。它在批准中间件之下工作，但**在**绝对阻止列表**之上**。

```bash
hermes --yolo
```

> ⚠️ `UNRECOVERABLE_BLOCKLIST` 中的命令（如 `rm -rf /`、fork 炸弹、直接块设备写入）无论是否使用 `--yolo` 或 `mode: off`，都**始终被阻止**。

---

## 选项 5：为非交互 / 子代理 / 子代理运行自动批准

当子代理遇到危险命令批准提示时，`subagent_auto_approve: false` 是默认值——自动拒绝。你可以将其设为 `true`，以自动批准 "一次"，而不是在" 而不是在 stdin 上阻塞。两种选择都会发出 `logger.warning` 审计行。仅对 cron/批处理流水线设为 `true`。

```yaml
# ~/.hermes/config.yaml
subagent_auto_approve: true
```

---

## 硬限制：UNRECOVERABLE_BLOCKLIST（不可恢复阻止列表）

无论你使用什么设置，某些命令具有灾难性——不可逆的文件系统擦除、fork 炸弹、直接块设备写入——Hermes 拒绝运行它们，无论设置如何。阻止列表在批准层甚至看到命令之前就会触发，并且没有覆盖标志。如果合法工作流需要这些命令之一，请在代理外部运行它。

---

## 总结表

| 方法 | 效果 | 风险级别 |
|---|---|---|
| `approvals.mode: off` | 无任何提示 | 高（主机暴露） |
| `approvals.mode: smart` | LLM 按命令决定 | 中 |
| Docker 后端 | 无提示 + 隔离 | 低（沙箱化） |
| `--yolo` 标志 | 跳过批准层 | 高 |
| `subagent_auto_approve: true` | 用于批处理/cron 流水线 | 中 |

**最佳实践：** 如果你想要零中断，请同时使用 `docker` 后端 + `approvals.mode: off`——你既能获得无提示的便利性，又能通过容器保护主机系统。

---

**参考资料：**

- [Hermes Agent 安全文档](https://hermes-agent.nousresearch.com/docs/user-guide/security)
- [Hermes Agent 配置文档](https://hermes-agent.nousresearch.com/docs/user-guide/configuration)
- [GitHub: cli-config.yaml.example](https://github.com/NousResearch/hermes-agent/blob/main/cli-config.yaml.example)
- [GitHub: 权限层级 Issue #527](https://github.com/NousResearch/hermes-agent/issues/527)