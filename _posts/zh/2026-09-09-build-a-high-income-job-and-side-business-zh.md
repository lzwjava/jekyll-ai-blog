---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 构建高收入工作与副业
translated: true
type: note
---

**问题：** 在当前的2026年创业/经济环境下，我应该是创业还是为一家公司工作——以及下一阶段对我来说最好的赚钱方式是什么？

**回答：**

我的观点是：**不要选择“创业 vs 工作”。选择一个高薪的AI工程职位 + 在业余时间打造一个具有创业形态的业务，只有当收入证明可行时，才全职投入创业。**

对于*你的特定情况*，我**不会**建议你立即辞职，花两年时间去打造一个投机性的初创公司。

### 1. 宏观环境实际上对你非常有利

AI不再处于“观望”阶段。

斯坦福大学2026年AI指数报告指出：

* 组织采用AI的比例达到了**88%**
* **79%** 的企业在至少一个业务功能中使用了生成式AI
* 2025年全球企业AI投资翻了一倍以上
* AI公司的收入增长极其迅速
* 但AI基础设施/计算成本也在爆炸式增长。([Stanford HAI][1])

与此同时，出现了一种奇怪的分化：

**AI的使用正在爆炸式增长，但通用软件工程的价值却在下降。**

斯坦福报告显示，22-25岁的软件开发人员就业率从2024年下降了近20%，并且三分之一的组织预计会出现与AI相关的劳动力削减。([Stanford HAI][1])

因此，我不会将你的下一阶段目标优化为：

> “成为一个更好的全栈工程师。”

我会优化为：

> **成为那些能让AI系统真正运行起来的人之一。**

这意味着：

```text
LLM
 ↓
推理
 ↓
CUDA / Triton
 ↓
GPU系统
 ↓
训练 / 后训练
 ↓
分布式系统
 ↓
AI产品
 ↓
收入
```

这个技术栈要难以商品化得多。

---

# 2. 我会选择“杠铃”策略

像这样：

```text
                 你
                  │
       ┌──────────┴──────────┐
       │                     │
   高薪工作              你的业务
       │                     │
   月薪                客户
       │                     │
   AI基础设施          咨询
   训练                代理
   推理                AI系统
   CUDA                产品
       │                     │
       └──────────┬──────────┘
                  │
             资本 + 技能
                  │
             创业选项
```

工作给你带来：

**现金 + 困难问题 + 人脉 + 信誉 + 技术成长**

业务给你带来：

**客户 + 分销渠道 + 所有权 + 非对称上升空间**

最终，如果业务开始产生：

```text
每月 5千美元
每月 1万美元
每月 2万美元
每月 3万美元
```

那么决定就变得容易了。

当**业务把你从雇佣关系中拉出来**时你再辞职，而不是辞职后指望业务能成功。

---

# 3. 先不要创办“初创公司”。先创造一个“现金机器”

这个区别很重要。

初创公司问的是：

> “我能建造一个价值1亿美元的东西吗？”

一个小的AI业务问的是：

> **“我能让一家公司付给我5000美元吗？”**

第二个问题要容易得多。

而在2026年，企业显然有资金投入到AI。与Gartner相关的研究报告称，85%的职能领导者计划在2026年增加AI支出，而许多公司仍在努力衡量投资回报率。([《华尔街日报》][2])

这正是机会所在。

公司需要的不是另一个：

```text
AI聊天机器人
AI包装应用
AI笔记应用
AI代理演示
```

他们需要的是：

```text
“我们有一个昂贵的业务流程。
你能把它自动化吗？”
```

这就是我会去发掘的方向。

---

# 4. 你最好的商业机会可能是AI工程服务 → 产品

你已经拥有一个不同寻常的组合：

```text
后端工程
        +
Python
        +
LLM
        +
训练
        +
GPU
        +
推理
        +
代理
```

大多数人只具备其中一两种技能。

你可以出售这个组合。

例如：

### AI推理优化

一家公司有：

```text
100个GPU
每月30万美元的推理账单
```

你进行优化：

```text
vLLM
KV缓存
量化
张量并行
CUDA
Triton
批处理
推测解码
MoE路由
GPU利用率
```

并为他们每月节省8万美元。

收费：

```text
2万美元的项目
```

完全是合理的。

---

### 私有/本地LLM部署

对于无法将数据发送给OpenAI/Anthropic的公司：

```text
客户
   ↓
他们的服务器
   ↓
开放权重模型
   ↓
vLLM
   ↓
RAG / 代理
   ↓
内部应用
```

你出售：

```text
部署
+
优化
+
微调
+
维护
```

这比构建另一个消费级AI应用更具防御性。

由于成本更低和可定制性，开放权重模型正变得越来越可行，而企业越来越多地基于经济性而非仅仅是基准分数来评估AI。([Business Insider][3])

---

# 5. 你对GPU的痴迷实际上可能很有用

你最近的工作涉及：

* RTX显卡
* GPU维修
* 显存
* CUDA
* 推理
* Triton
* FreeToken
* MoE
* MXFP4
* KV缓存
* 多GPU
* 训练

看起来有些分散。

但我看到了一个潜在的基础方向：

> **AI计算工程**

这是一个真实的行业。

AI基础设施支出巨大。例如，英伟达仍在预测极其强劲的增长，而HPE和CoreWeave则看到了巨大的AI基础设施需求。([Reuters][4])

你不需要成为英伟达。

你可以坐落在上一层/下一层：

```text
英伟达
   ↓
GPU / 硬件
   ↓
云 / 服务器
   ↓
AI基础设施
   ↓
你
   ↓
客户
```

潜在的生意：

```text
GPU优化咨询
AI推理优化
私有LLM部署
GPU集群搭建
模型量化
训练优化
AI代理基础设施
AI迁移咨询
```

---

# 6. 但我仍然会找一份更好的AI工作

如果你能找到一份收入远高于当前职位的工作，我会接受它，**前提是技术密度很高**。

不要只为薪水而优化。

我大致会这样排序机会：

| 机会                                | 对你的价值       |
| ----------------------------------- | --------------: |
| 前沿AI / AI基础设施工程师           |        ⭐⭐⭐⭐⭐ |
| LLM推理/训练工程师                  |        ⭐⭐⭐⭐⭐ |
| GPU/CUDA系统工程师                  |        ⭐⭐⭐⭐⭐ |
| 拥有强大技术团队的AI初创公司        |        ⭐⭐⭐⭐⭐ |
| 企业AI工程师                        |         ⭐⭐⭐⭐ |
| 通用后端工程师                      |           ⭐⭐ |
| 通用全栈工程师                      |            ⭐ |
| 传统CRUD外包                        |            ⭐ |

你的目标不仅仅是：

> “每月赚4万人民币。”

而是：

> **具备利用AI专业知识每月创造1万至10万美元收入的能力。**

雇佣关系是利用这种能力变现的一种方式。

所有权是另一种。

---

# 7. 我会慎重地利用接下来的两年

我建议的路线：

### 第一阶段 — 接下来的6个月

**工作 + 积极的AI专业化**

深入学习：

```text
PyTorch
CUDA
Triton
vLLM
DeepSpeed
Megatron
FSDP
MoE
量化
KV缓存
推测解码
分布式训练
推理优化
```

但不要只是学术性地学习。

要动手构建东西。

例如：

```bash
git clone your-own-llm-runtime

# 实现
attention
kv-cache
paged-attention
moe
tp
quantization
speculative-decoding
```

你的GitHub将成为你的作品集。

---

### 第二阶段 — 同时进行

开始销售你的工程能力。

不是说：

> “我经营一家AI公司。”

而是：

> “我可以降低你的LLM推理成本/部署你的私有模型/优化你的GPU工作负载。”

找到20家公司。

与他们交谈。

你的第一个目标：

```text
1000美元
```

然后：

```text
5000美元
```

然后：

```text
每月1万美元
```

---

### 第三阶段 — 6到18个月

寻找可重复性。

假设你发现：

```text
客户A：
GPU推理优化

客户B：
GPU推理优化

客户C：
GPU推理优化

客户D：
GPU推理优化
```

现在你有了抓手。

将：

```text
咨询
```

转化为：

```text
服务
```

然后：

```text
产品化服务
```

最后：

```text
软件
```

这比从零发明一个SaaS产品要安全得多。

---

# 8. 你可能犯的最大错误是过早开始构建

你有足够的技术能力，可以埋头搞工程长达12个月。

那是危险的。

你可能花费：

```text
3个月 → CUDA
2个月 → 推理
3个月 → 模型训练
2个月 → 代理
2个月 → 产品
```

最终的结果是：

```text
0美元收入
```

市场不奖励技术复杂性。

它奖励的是：

```text
痛点 × 支付意愿 × 分销能力
```

所以我会强迫自己进入这个循环：

```text
与客户交谈
      ↓
找到痛点问题
      ↓
出售解决方案
      ↓
构建最小化解决方案
      ↓
交付
      ↓
获得报酬
      ↓
重复
      ↓
自动化
      ↓
产品化
```

---

# 9. 那风投支持的初创公司呢？

**暂时不要，除非你发现了一个异常强劲的机会。**

初创公司的融资环境对AI来说仍然非常强劲。例如，Cognition公司刚刚以480亿美元的估值融资20亿美元。([Reuters][5])

但这并不意味着**你**应该去筹集风投资金。

风投在以下情况是合适的：

```text
市场巨大
+
产品有强大的吸引力
+
增长极其迅速
+
资本能加速业务发展
```

仅仅因为以下原因是不合适的：

```text
“我想成为一名创始人。”
```

如果你能用2-3个人、高利润率每月赚到：

```text
2万美元
```

那已经是一门很不错的生意了。

你不需要1亿美元的估值。

---

# 10. 真正的游戏：增加你的“赚钱表面积”

我认为这是对你最重要的概念。

不要想：

> 工作 或 创业。

要想：

```text
                 赚钱表面积
                       │
       ┌───────────────┼────────────────┐
       │               │                │
     薪资            咨询             股权
       │               │                │
  每月4万RMB      每月1万RMB         初创公司
       │               │                │
       └───────────────┼────────────────┘
                       │
                  AI专业知识
```

随着时间的推移：

```text
2026年
薪资        ██████████
咨询        ██
股权        ▏

2027年
薪资        ████████
咨询        █████
股权        ██

2028年
薪资        ████
咨询        ███████
股权        ███████████
```

你从**出售时间**逐渐过渡到**出售系统**再到**拥有资产**。

---

# 我对你的建议

如果我凭你目前的状况来做决定，我会这样安排：

```text
2026–2027

        高端AI工作
             +
       AI咨询
             +
       公开的技术工作
             +
         小型产品
```

目标：

```text
工作：             年薪6万至10万美元以上
咨询：             年薪3万至10万美元以上
产品：             可选
股权：             上升空间
```

然后重新评估。

如果咨询/产品收入达到：

```text
每月1万美元 → 认真考虑
每月2万美元 → 非常认真
每月3万美元以上 → 考虑离职
```

到那时，**你不需要问是否应该创办公司。你已经拥有了一个。**

当前的AI经济为你提供了一个特别好的切入点，因为大量资本正涌入AI基础设施和企业部署，而各组织正在努力将AI支出转化为可衡量的投资回报率。([Stanford HAI][1])

所以我的一行回答是：

> **不要用你的现金流去赌一个初创公司。先成为一名异常强大的AI系统工程师，为此获得高薪，然后将同样的专业知识直接出售给公司，让客户的收入告诉你何时该成为全职创始人。**

而且我会特别将你定位在**LLM推理/训练 + GPU系统 + AI代理**领域，而不是通用的“AI应用开发”。

### 参考文献

* [Stanford AI Index 2026 — Economy](https://hai.stanford.edu/ai-index/2026-ai-index-report/economy?utm_source=chatgpt.com)
* [Stanford AI Index 2026](https://hai.stanford.edu/ai-index/2026-ai-index-report?utm_source=chatgpt.com)
* [Reuters — Cognition raises $2B at $48B valuation](https://www.reuters.com/technology/cognition-ai-raises-2-billion-48-billion-valuation-2026-09-08/?utm_source=chatgpt.com)
* [Reuters — Nvidia forecasts continued AI growth](https://www.reuters.com/business/media-telecom/nvidia-forecasts-quarterly-revenue-above-estimates-2026-08-26/?utm_source=chatgpt.com)

[1]: https://hai.stanford.edu/ai-index/2026-ai-index-report/economy?utm_source=chatgpt.com "Economy | The 2026 AI Index Report | Stanford HAI"
[2]: https://www.wsj.com/tech/ai/ai-spending-is-up-so-is-the-guesswork-93cf1f36?utm_source=chatgpt.com "AI Spending Is Up. So Is the Guesswork."
[3]: https://www.businessinsider.com/nea-partner-aaron-jacobson-weighs-in-on-open-versus-closed-2026-9?utm_source=chatgpt.com "An NEA partner says not every AI task needs frontier intelligence"
[4]: https://www.reuters.com/business/media-telecom/nvidia-forecasts-quarterly-revenue-above-estimates-2026-08-26/?utm_source=chatgpt.com "Nvidia forecasts 70% sales growth next year, signals AI spending boom has years left to run"
[5]: https://www.reuters.com/technology/cognition-ai-raises-2-billion-48-billion-valuation-2026-09-08/?utm_source=chatgpt.com "Cognition AI raises $2 billion at $48 billion valuation"
