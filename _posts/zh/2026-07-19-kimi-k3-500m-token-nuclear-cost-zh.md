---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Kimi K3：5亿令牌核成本
translated: true
type: note
---

问题：什么是“5亿Token实测Kimi K3：我看到了核弹，也看到高昂的成本”？

回答：

这是一篇关于**大规模实测Kimi K3**的文章/标题，作者使用该模型消耗了**5亿token**（约5e8 tokens），并得出结论：

> Kimi K3 极其强大（“核弹”），但经济性昂贵（“高昂的成本”）。

Kimi K3 是月之暗面（Moonshot AI）的新旗舰模型。据报道，它是一个**2.8万亿参数的MoE模型**，拥有非常大的上下文窗口（约100万token）。（[Tom's Hardware][1]）

文章的核心观点大概是：

## 1. “核弹” = 能力震撼

作者很可能在真实工作负载上测试了K3：

* 编程代理（coding agents）
* 长文档处理
* 研究任务
* 多步推理
* 自主工作流

令人惊讶的是：

* 它能够容纳巨大的上下文
* 它能够生成大量代码
* 它能够推理复杂任务
* 它表现更接近前沿闭源模型

这就是为什么人们用“核武器”来比喻它。

据报道，K3在编程基准测试（包括前端编码评估）中表现非常强劲，与顶级闭源模型一较高下。（[Decrypt][2]）

---

## 2. “5亿Token”实际上是一次严肃的测试

5亿token是一个巨大的数字。

大致估算：

```
5亿token

≈ 3.75亿英文单词
≈ 数百万页文本
≈ 数千次长代码会话
```

对AI工程师来说，这更接近：

```
普通用户：
    每月10万token

高级用户：
    每月1000万token

代理开发者：
    每月1亿+ token

疯狂评估：
    5亿token
```

所以作者并不是说：

> “我和Kimi聊了一周。”

更像是：

> “我把Kimi集成到工作流中，并测量了类似生产环境的用量。”

---

## 3. 为什么昂贵？

问题不仅仅是API价格。

报道的K3定价：

```
输入：
每百万token 3美元

输出：
每百万token 15美元
```

缓存输入便宜得多：

```
每百万缓存token 0.30美元
```

（[TheQuery][3]）

现在计算：

### 5亿token

如果大部分是输出：

```
5亿 / 100万 * 15美元

= 7,500美元
```

如果大部分是输入：

```
5亿 / 100万 * 3美元

= 1,500美元
```

实际代理使用是混合的。

可能是：

```
输入 4亿
输出 1亿

400 * 3美元
+
100 * 15美元

= 1,200美元 + 1,500美元

≈ 2,700美元
```

所以一次严肃的开发者测试很容易花费数千美元。

---

## 4. 有趣的工程要点

K3显示了一个新趋势：

以前：

```
开源模型优势：
便宜
```

DeepSeek风格：

```
足够好的智能
+
极低价格
```

现在K3：

```
前沿智能
+
巨大上下文
+
代理能力

但

不便宜
```

竞争正在从：

> “谁的LLM最便宜？”

转向：

> “谁的每完成任务的成本最低？”

示例：

一个成本高5倍但能一次性完成编码任务的模型，可能比一个需要10次重试的弱模型更便宜。

---

## 5. 我对你用例（LLM工程）的看法

对于构建代理/训练/评估模型的人来说：

K3很有趣，因为它改变了开源模型的天花板。

但我不会用K3取代一切。

一个实用的路由方案：

```
简单任务：
    Qwen / DeepSeek / 更便宜的模型

编码：
    Claude / GPT / Kimi K3

长上下文：
    Kimi K3

本地：
    较小的开源模型
```

最大的问题不是基准分数。

真正的考验：

```
每次成功合并PR的成本
每次解决bug的成本
每次自主完成任务完成的成本
```

这才是代理模型胜负的关键。

参考资料：

* （[Tom's Hardware][1]）
* （[TheQuery][3]）
* （[LLM Rumors][4]）
* （[The Decoder][5]）

[1]: https://www.tomshardware.com/tech-industry/artificial-intelligence/moonshot-releases-2-8-trillion-parameter-kimi-k3?utm_source=chatgpt.com "中国2.8万亿参数的Kimi K3在Frontend Code Arena基准测试中击败Claude Fable 5——月之暗面发布史上最大的开放权重AI模型，中国绕过美国计算限制 | Tom's Hardware"
[2]: https://decrypt.co/373716/china-kimi-k3-largest-open-source-ai-model-ever-beats-claude-fable-gpt-5-6-sol?utm_source=chatgpt.com "中国的Kimi K3发布——在关键基准测试中击败Claude Fable和GPT 5.6 Sol - Decrypt"
[3]: https://www.thequery.in/articles/kimi-k3-largest-open-weight-model-claude-opus-gpt-55?utm_source=chatgpt.com "Kimi K3是迄今为止宣布的最大开放权重模型。它还击败了Claude Opus 4.8和GPT-5.5。| TheQuery"
[4]: https://www.llmrumors.com/news/kimi-k3-open-model-champion-in-waiting?utm_source=chatgpt.com "Kimi K3基准测试、定价、API和开放权重 | LLM Rumors"
[5]: https://the-decoder.com/kimis-open-model-k3-nears-gpt-5-6-sol-and-fable-5-while-signaling-the-end-of-super-cheap-chinese-ai/?utm_source=chatgpt.com "Kimi的开放模型K3接近GPT-5.6 Sol和Fable 5，同时预示着超便宜中国AI的终结"
