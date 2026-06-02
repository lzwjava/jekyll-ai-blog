---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Claude 4 Sonnet模型性能指标详解
translated: true
type: note
---

简而言之：这是正常结束。
`finish_reason: "stop"` 表示模型已自然完成回复（遇到停止序列如assistant-end标记），且**未**触发长度限制、错误或取消。

以下是该记录其余字段的通俗解释：

* **模型与路由**
  您通过**Google Vertex**（`provider_name: "Google"`）调用了**anthropic/claude-4-sonnet-20250522**。因此会看到状态码为200的`provider_responses`条目。

* **耗时/速度**

  * `latency: 2850` → 约**2.85秒**后出现**首个令牌**
  * `generation_time: 76365` → 完整生成回复总计约**76.4秒**
  * 结合`tokens_completion: 2376`，可推算出全程生成速率约**31令牌/秒**（2376 ÷ 76.4 ≈ 31.1）

* **令牌计数（双体系）**

  * `tokens_prompt: 8446`、`tokens_completion: 2376` → 聚合器统计值
  * `native_tokens_prompt: 9007`、`native_tokens_completion: 2511` → **服务商**自有分词器的统计。因分词器差异、系统封装或隐藏控制令牌等因素，两组数值常不同
  * `native_tokens_reasoning: 0` → 未启用"推理令牌"计量（部分服务商在特殊推理模式下会显示）
  * `native_tokens_cached: 0` → 未命中提示词缓存

* **流式传输与取消**

  * `streamed: true` → 采用流式传输
  * `cancelled: false` → 未中途取消

* **为何不是"length"？**
  若触及令牌上限，将显示`finish_reason: "length"`。当前记录未触发该限制。

* **发生时间**
  `created_at: "2025-09-02T17:26:45.92824+00:00"`（UTC时间）。换算为您所在时区（亚洲/台北，UTC+8）为**2025-09-03 01:26:45**。

* **费用/用量字段**

  * `usage: 0.064686` → 系统内部计费指标（单位取决于结算层级）
  * 多个`null`字段表示路由未记录额外信息（审核延迟、搜索结果等）

* **其他**

  * `finish_reason: "stop"`（再次强调）是关键：通过停止标记正常终止
  * `origin: ""`、`app_id: null` → 未标记特定应用来源
  * `is_byok: false` → 非自带密钥调用

如果您需要，可以粘贴另一个显示`length`或`cancelled`的示例，我将逐行对比解析（无需表格形式）。
