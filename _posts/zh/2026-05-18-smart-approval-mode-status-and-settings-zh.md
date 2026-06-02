---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 智能审批模式状态与设置
translated: true
type: note
---

您的配置确认在第406行设置了`approvals.mode: smart`。当前状态如下：

**配置文件 (~/.hermes/config.yaml)：**

- `approvals.mode: smart` -- 已设置（第406行）
- `approvals.timeout: 60` -- 已设置（第407行）
- `approvals.cron_mode: deny` -- （第408行）
- `auxiliary.approval.provider: auto` -- （第198行，用于智能评估的LLM）

**在当前会话中生效？**

是的。配置文件在会话启动时读取，因此您当前的会话已激活`smart`模式。当命令匹配危险模式时，Hermes不会立即提示您，而是调用辅助审批LLM评估风险。如果LLM判定命令安全，则自动放行。仅真正有风险的命令会触发提示。

**关于您配置的关键细节：**

- `auxiliary.approval.provider: auto` 表示它继承您的主提供者（openrouter），并选择一个轻量/低成本模型用于风险评估调用。
- `subagent_auto_approve: false`（第348行）——子代理将不会自动批准危险命令，而是会被拒绝。如果您希望批量/定时任务无需等待审批直接执行，请将该值改为`true`。
- `terminal.backend: local`（第67行）——您直接在主机上运行命令，因此危险命令检查仍然有效（在Docker容器后端中则会跳过此项）。

如果您发现`smart`模式仍过于频繁地提示，下一步可考虑`mode: off`。但结合`smart`模式与`local`后端，您可以获得合理的平衡：LLM过滤误报，同时捕捉真正危险的操作。
