---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Kimi K3 的低 OpenRouter 排名
translated: true
type: note
---

**问题：** 为什么 Kimi K3（23B/大模型）在 OpenRouter 上排名不高？用户是否只是直接订阅 Kimi 服务？

**回答：**

你的直觉基本正确，但有几个影响因素。

首先，**Kimi K3 并非典型的“廉价 OpenRouter 模型”**。它被定位为前沿模型。Moonshot 推出 Kimi K3 作为一个非常大的开放权重模型（据报告总参数 2.8T MoE，上下文 1M），目标是长时编程/推理，而非廉价日常对话。（[路透社][1]）

OpenRouter 排名主要反映**使用量**，而非“最佳模型”。一个模型可能非常优秀，但排名不高，原因如下：

1. **对于 API 用户来说价格过高**

如果 API 用户进行对比：

* DeepSeek / Qwen 系列模型：极其便宜
* Kimi K3：接近前沿高价水平

据报告，Kimi K3 的 API 定价约为：

```
输入：$3 / 1M tokens
输出：$15 / 1M tokens
缓存命中：$0.30 / 1M
```

（[RouterPlex][2]）

对于智能体循环：

```
用户提示
 → 模型思考
 → 工具调用
 → 模型思考
 → 重试
 → 总结
```

输出 tokens 占主导。$15/M 的输出成本令人望而却步。

OpenRouter 大量流量来自：

* 编程智能体
* 批量生成
* 个人爱好者
* 评估脚本

他们关注每任务成本。

---

2. **Kimi 用户可能留在 Kimi 生态系统内**

是的，这是一个重要因素。

Moonshot 拥有：

* kimi.com
* Kimi Code
* 订阅计划

最佳的 Kimi 体验可能在其原生产品中，因为他们可以控制：

```
模型
+
系统提示
+
工具调用
+
上下文管理
+
配额
+
缓存
```

第三方 API 会失去部分优势。

Kimi Code 文档显示 K3 直接集成到其编程环境中，具有特殊的模型 ID 和上下文处理方式。（[Kimi][3]）

因此，付费订阅 Kimi 的开发者可能根本不会碰 OpenRouter。

---

3. **OpenRouter 排名存在冷启动问题**

新模型通常：

```
发布
 ↓
供应商少
 ↓
价格高
 ↓
用户尝试一次
 ↓
流量低
 ↓
排名低
```

有报告称，早期 OpenRouter 上 K3 的可用性有限，且供应商过载。（[Reddit][4]）

---

4. 关于“23B”的误解

如果你指的是**23B 激活参数**，那实际上是 MoE 的激活计算量，而非模型总大小。

现代 MoE：

```
总参数：2.8T
每 token 激活：~20-30B
```

类似概念：

```
DeepSeek V3：
总参数 671B
激活 37B
```

重要指标是：

```
质量 / 激活 FLOPs / 美元
```

而非总参数数量。

---

我目前的看法：

Kimi K3 可能是一项**技术成就**，但商业定位存在疑问：

```
封闭前沿：
 GPT / Claude
      |
      | 更好的用户体验 + 可靠性
      |
Kimi K3
      |
      | 昂贵的开放模型
      |
廉价开放模型：
 DeepSeek / Qwen
```

危险的中间地带是：

* 不如 DeepSeek 便宜
* 不如 Claude/OpenAI 生态成熟
* 对于自部署来说太大

开放模型的制胜策略可能是：

```
足够小以部署
+
足够便宜以运行
+
对智能体足够好
```

例如：

* Qwen 30B/70B 级别
* DeepSeek 蒸馏模型
* 未来的 20-50B MoE 模型

如果以下条件成立，Kimi K3 可能获胜：

```
质量接近 Claude/GPT
且
Moonshot 补贴 API 成本
且
开放权重确实可用
```

否则，许多用户只会说：

“基准测试很厉害，但我还是会用 DeepSeek/Qwen，因为我的智能体每天跑 1000 次调用。”

[1]: https://www.reuters.com/world/china/chinas-moonshot-unveils-worlds-largest-open-ai-model-closing-us-rivals-2026-07-17/?utm_source=chatgpt.com "中国 Moonshot 发布全球最大开放 AI 模型，逼近美国竞争对手"
[2]: https://routerplex.com/blog/kimi-k3-api-pricing-setup?utm_source=chatgpt.com "Kimi K3 API：定价、上下文窗口和设置 · RouterPlex"
[3]: https://www.kimi.com/code/docs/en/kimi-code/models.html?utm_source=chatgpt.com "模型配置 | Kimi Code 文档"
[4]: https://www.reddit.com/r/openrouter/comments/1uye4ec/kimi_k3_is_now_on_openrouter/?utm_source=chatgpt.com "Kimi K3 现已登陆 OpenRouter"
