---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 重启以应用配置更改
translated: true
type: note
---

运作原理如下：

**配置仅在创建 agent 时读取一次。** `max_tokens` 的值在 `init_agent()` 时设定，并在 CLI 进程的整个生命周期内保持不变。

**各操作的具体效果：**

| 操作 | 是否重新读取配置？ | 是否应用新的 `max_tokens`？ |
|---|---|---|
| `/clear` 或 `/new` | 否 — 使用同一 agent 对象 | 否 |
| `/model` 切换到不同模型 | 是 — 重新创建 agent | 是（如果切换离开后再切回来） |
| **Ctrl+C + 重启** | **是 — 全新进程** | **是** |

只有当路由签名（model + provider + base_url + api_mode）发生变化时，agent 才会被重新创建。在 config.yaml 中修改 `max_tokens` 不会改变签名，因此 `/clear` 无效。

**简而言之：使用 Ctrl+C 退出 CLI 并重新启动。** 这是可靠的方式。
