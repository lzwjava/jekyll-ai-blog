---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 缺少azure/gpt-5.5的通道
translated: true
type: note
---

错误并非来自 Hermes——而是 **ORG2** 试图通过 new-api/one-api 反向代理调用 `azure/gpt-5.5` 所导致的。中文错误信息：

```
分组 default 下模型 azure/gpt-5.5 无可用渠道（distributor）
```

意思是：**"模型 azure/gpt-5.5 在 'default' 分组下没有可用渠道"**

这是 API 代理端的后端配置问题，并非 ORG2 的代码错误。


## 修复方法

**选项 1 — 在 ORG2 中更换模型**

在 ORG2 应用中，前往设置 → Provider/Model 设置，将 `azure/gpt-5.5` 切换为代理中实际存在的模型。如果你的代理后端是 Azure OpenAI，常见可用模型包括：
- `azure/gpt-4o`
- `azure/gpt-4o-mini`
- `azure/gpt-4.1`

**选项 2 — 在 new-api/one-api 代理中添加该模型**

如果你正在运行 new-api 或 one-api 实例：
1. 登录代理管理面板
2. 前往渠道 → 编辑 Azure 渠道
3. 在模型列表中添加 `gpt-5.5`（或检查该模型名称是否真实存在——目前 OpenAI/Azure 并没有 `gpt-5.5`）
4. 确保渠道已启用且状态正常

**选项 3 — 检查模型名称是否正确**

`gpt-5.5` 并非已知的 OpenAI/Azure 模型。如果你实际意图是：
- `gpt-4.5` → 某些区域可作为 Azure 模型使用
- `o3` / `o4-mini` → 推理模型
- `gpt-4o` → 最常用

请更新 ORG2 中的模型名称，使其与代理实际支持的模型一致。


## 总结

你的 API 代理（new-api/one-api）没有为 `azure/gpt-5.5` 配置渠道。要么在 ORG2 设置中修正模型名称，要么在代理的渠道配置中添加该模型。当前显示“重新连接”状态是因为 ORG2 正在不断重试失败的请求。