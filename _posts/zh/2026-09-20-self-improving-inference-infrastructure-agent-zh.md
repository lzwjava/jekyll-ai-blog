---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 自我改进的推理基础设施智能体
translated: true
type: note
---

问题：**阅读并解释 Z.ai 的《走向递归式自我改进：GLM 如何构建自己的推理基础设施》。**

回答：

我阅读了这篇文章。重点其实**不在于“GLM 写了一个推理服务器”**。有趣的是工程循环：

> **GLM-5.3 变成了一个能够检查、修改、基准测试、调试和优化运行 GLM-5.3-Flash 的基础设施的智能体。**

Z.ai 表示，生产系统运行在 **超过 100,000 个中国 AI 加速器** 上，从首次成功运行到投产只用了 **不到两周**，并且与初始基准相比，实现了大约 **3 倍的端到端吞吐量**。([GIGAZINE][1])

![图片](https://images.openai.com/static-rsc-4/Xfgm7h8i8QjxjkFtiAVPZ9qhEd3Ygt98E9Su4kNbJEtLHZIGY_tvHBPsIkE0V0r4Yf4KHoZdME0Ew0kN1kZMIQjv9KshYDRTb4qB1eS_un5eVfGaROSV7lcab9zORM8eRwMzEZd56yvM4F7kB0xiWVaxBifJd2EhVyeHj9Jt_ie10WtxXwWDj3Il71iFK7tT?purpose=fullsize)

![图片](https://images.openai.com/static-rsc-4/vcj4XWpdk85vhZh8M6TTqcX-m4AsS_dhVXjoitYgjNqx1ugPDvemzl4kFB0R5USaJnU8qwxbVTGy5QWzjSdSkuYIbxOn0_iKUbk_IG-O0FY2zAnRTgPzoR2_EWPn4WSCiO9gmIAh_QojNTXI3_OylE7YfPcZCALC09M4tTULpb7ZHGRoDkl7njaTBrL8If_8?purpose=fullsize)

![图片](https://images.openai.com/static-rsc-4/KZeWg_-m5gy5m9V4gB1swz7L2SyXzET6OIT6udH9lZEHVKkH5ppKN2Z2n6OUb0mCZ-vnMnFwqd8uo5K6vlLbIxe911y13edk0SBKbRcMV-gS3MttCniT5xcCNPJZqEt6KOEYULSQ8AB-n3U0EqBrGlo8p76SuqCVW319o_Yk9F_oGE5OXAYs7x_wgghsqNlJ?purpose=fullsize)

![图片](https://images.openai.com/static-rsc-4/E_nZE3o-3N8NMD_LMyLvdhXaoxciL79ekE4XrFg1adgISIXWA-KFQFL8jDGwjsNE0DcRft9CtdIu9VgYEFmw2HH3_0nXkof6Vrh8k73qEzPRoGItoxFe6q2fBoU9UzCpNseqiTBBCxyVrtJZROEPrI1iRPxPVX-hqIqfwcA_IOx-h1GpVT8uoMsxSI3-11AU?purpose=fullsize)

![图片](https://images.openai.com/static-rsc-4/7earB_p78zoA4wXeP8z8cN6Kz1Rwrs_PDUV5Zp3Ui6XMx5GuJ-pKKirTi4zGOUaRgnI_1V3UZB_k1P8ek-pqj3joU4qwj5_ddELt6M0ueYS8KrucMgaxnuqIxzJkNHsS09FoIKxOocShuPZfLoUzKg2LBAN2d06-PYyDAXTSTjaH2IuuCbKVUyrD5hmIpH-K?purpose=fullsize)

![图片](https://images.openai.com/static-rsc-4/Oj36W42OPcR8yN5UuZ0zQ9poLZ-N-YWtBP4GA5y9tHNC9g-rxHIbvbl-PpunbZY_Hg94i1lDHHeZjWHbdeSxegm-eQ_R6Aciez23kQ7ACfjRp9c-JKyNkN2ZVEIRkXhXRoeqUQkuq-t893OTDY9Cx_99y8kH8Cptoa6eY0_PR6OUdfZv5Mj0jdQg1TzBtBqv?purpose=fullsize)

### 1. 核心思想：将基础设施优化转化为类似强化学习的反馈循环

传统优化看起来像这样：

```text
人类工程师
    ↓
理解瓶颈
    ↓
修改 C++ / CUDA / 内核 / 调度器
    ↓
基准测试
    ↓
检查结果
    ↓
重复
```

Z.ai 基本上将其转变为：

```text
                 ┌──────────────┐
                 │  GLM-5.3     │
                 │ 基础设施智能体│
                 └──────┬───────┘
                        │
                 检查系统
                        ↓
              生成假设
                        ↓
                 修改代码
                        ↓
              运行正确性测试
                        ↓
                运行微基准测试
                        ↓
                运行端到端测试
                        ↓
                  观察指标
                        │
                 ┌──────┴──────┐
                 │             │
              更好           更差
                 │             │
              保留           拒绝
                 │
                 └──────→ 下一个实验
```

这种**密集反馈**是关键。这个智能体不仅仅是被告知：

> “让推理更快。”

它可以访问本地正确性测试、执行跟踪、微基准测试和端到端测量，使其能够测试具体的假设。([Tech Twitter][2])

这非常接近你最近问到的关于**可验证奖励**的原则：

```text
模型
  → 行动
  → 可执行环境
  → 客观测量
  → 奖励 / 反馈
  → 下一个行动
```

只不过这里的环境是**一个巨大的推理系统**，而不是 Lean 或编码基准。

---

### 2. 为什么推理基础设施特别适合智能体

这是更深刻的见解。

很多软件工程的奖励信号很弱：

```text
“这段代码好吗？”
```

难以自动衡量。

但推理基础设施有非常具体的目标：

```text
正确性       = 通过 / 失败
延迟           = 毫秒
吞吐量       = tokens / 秒
GPU 利用率   = %
内存            = GB
通信           = GB/秒
内核时间      = μs
成本           = $ / 1M tokens
```

因此智能体所处的环境是**可测量的**。

例如：

```python
候选 = 智能体.修改(代码)

正确 = 运行测试(候选)

如果 正确:
    吞吐量 = 基准测试(候选)

    如果 吞吐量 > 基线:
        保留(候选)
    否则:
        还原(候选)
否则:
    还原(候选)
```

这比让智能体改进类似这样的东西要容易自动化得多：

```text
“让架构更优雅”
```

后者没有清晰的验证器。

---

### 3. 这个智能体深入到了技术栈中

根据已发布的说明和二手技术摘要，这项工作不仅仅是 Python 胶水。

优化的范围包括：

```text
模型图
   ↓
并行性
   ↓
量化
   ↓
KV 缓存
   ↓
调度器
   ↓
Python 运行时
   ↓
C++ 运行时
   ↓
自定义内核
   ↓
加速器
   ↓
分布式通信
```

报告的技术包括张量并行、W8A8 量化、混合精度缓存，以及分离编码 / 预填充 / 解码工作负载。([Koko Knows][3])

这很重要，因为**推理优化是跨层优化**。

瓶颈可能看起来像：

```text
GPU 利用率：70%
```

但实际原因可能是：

```text
Python 锁
   ↓
C++ 工作进程被阻塞
   ↓
通信延迟
   ↓
加速器空闲
   ↓
GPU 利用率低
```

一个报道的例子是传输性能问题，追溯到 Python/C++ 并发；修复锁行为后，性能差距据报道从 >20% 降到了 <1%。([Reddit][4])

这正是智能体使用以下工具可以发挥巨大作用的任务类型：

```text
grep
perf
跟踪
基准测试
编译器
测试
日志
git
```

---

### 4. 另一个有趣的例子：内核优化

据报道，该智能体在一个关键内核中发现了冗余计算并重新设计，获得了该阶段约 **1.71 倍的加速**。([Reddit][4])

想想搜索空间：

```text
内核 v1
   ↓
性能分析
   ↓
智能体注意到冗余操作
   ↓
假设
   ↓
重写内核
   ↓
编译
   ↓
正确性测试
   ↓
微基准测试
   ↓
1.71×
   ↓
保留
```

人类不一定需要明确告诉它：

> “看看这个内核的第 483 行。”

模型可以自行浏览代码库 + 分析器输出 + 基准测试结果。

这比普通的“AI 编码”能力有趣得多。

---

## 5. 这个架构本质上是一个自动化的科学方法

这是我如何抽象整个 Z.ai 系统的：

```text
                  ┌──────────────┐
                  │   目标       │
                  │ 最大化      │
                  │ 吞吐量      │
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │   观察       │
                  │ 跟踪/日志    │
                  │ 配置文件     │
                  │ 基准测试     │
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │  假设        │
                  │ “瓶颈是 X”   │
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │    修改      │
                  │ 代码/内核    │
                  │ 配置         │
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │    执行      │
                  │ 测试 +       │
                  │ 基准测试     │
                  └──────┬───────┘
                         ↓
                  ┌──────────────┐
                  │   测量       │
                  └──────┬───────┘
                         ↓
                    下一次迭代
```

这基本上就是：

**LLM + 编译器 + 分析器 + 基准测试 + 模拟器 + 测试套件 + git = 工程研究智能体。**

---

## 6. 为什么“递归式自我改进”不是完全字面上的意思

这是我要谨慎的地方。

标题说：

> **走向**递归式自我改进

而不是：

> “我们实现了递归式自我改进。”

Z.ai 报道的设置仍然需要人类定义：

```text
目标
约束
测试
系统边界
验收标准
生产部署
```

智能体在**该环境内**进行优化。它并不是独立决定：

```text
“GLM 应该变成什么？”
```

然后自我训练，重新设计模型架构，分配计算资源，启动新模型，并在没有人类干预的情况下取代它的前身。

一个更好的描述是：

```text
AI 辅助的递归式工程循环
```

而不是完全的：

```text
AI 递归地自我改进
```

独立的摘要也强调了这一区别。([Ground Truth][5])

---

# 7. 但这里有一个真正有趣的 RSI 方向

想象扩展这个循环。

今天：

```text
GLM-5.3
   ↓
优化
   ↓
推理基础设施
```

下一步：

```text
GLM
 ↓
优化推理
 ↓
更便宜的推理
 ↓
更多实验
 ↓
更好的训练
 ↓
更好的模型
```

然后：

```text
更好的模型
    ↓
更好的编码智能体
    ↓
更好的基础设施优化
    ↓
更便宜的计算
    ↓
更多的训练 / 实验
    ↓
更好的模型
```

现在你有了一个正反馈循环：

$$
M_{t+1}=f(M_t,\ C_t,\ E_t)
$$

其中：

* \\(M_t\\) = 模型能力
* \\(C_t\\) = 可用计算资源
* \\(E_t\\) = 工程环境

而基础设施优化可以增加有效计算量：

$$
C_{\mathrm{有效}}
=
C_{\mathrm{硬件}}\times
\eta_{\mathrm{软件}}
$$

如果智能体将服务/训练效率从 \\(1\times\\) 提高到 \\(3\times\\)，你实际上是在不给研究过程额外购买 \\(2\times\\)–\\(3\times\\) 集群的情况下，大幅增加了计算量。

这就是为什么这很重要。

---

# 8. 对你作为基础设施/智能体构建者最重要的教训

我认为最有用的收获不是：

> “GLM 非常强大。”

而是：

> **构建能让智能体获得客观反馈的环境。**

例如，不要只构建一个写 CUDA 的智能体：

```text
提示词
 ↓
LLM
 ↓
CUDA 代码
```

而是构建：

```text
                 ┌───────────────┐
                 │      LLM      │
                 └───────┬───────┘
                         ↓
                 修改实现
                         ↓
              ┌─────────────────────┐
              │ 可复现的运行器       │
              └──────────┬──────────┘
                         ↓
             正确性 + 基准测试
                         ↓
                ┌────────────────┐
                │ 客观指标       │
                │ 吞吐量         │
                │ 延迟           │
                │ 内存           │
                │ 成本           │
                └───────┬────────┘
                        ↓
                   LLM 看到结果
                        ↓
                     迭代
```

这基本上是**通过可执行反馈进行的智能体系统研究**。

这与你在 `nano-vLLM`、CUDA、MTP/KV 缓存、GPU 修复和推理优化方面的工作直接相关：**环境越可测量，你能安全地给予智能体的自主权就越多。**

Z.ai 的文章之所以有价值，正是因为它在大规模生产中展示了这种模式，而不仅仅是展示了一个 LLM 生成一些推理代码。([GIGAZINE][1])

**参考文献：**

* [Z.ai — 走向递归式自我改进：GLM 如何构建自己的推理基础设施](https://z.ai/blog/glm-built-its-inference-infrastructure?utm_source=chatgpt.com)
* [GIGAZINE — Z.ai 的 100,000+ 加速器部署摘要](https://gigazine.net/gsc_news/en/20260918-how-glm-built-inference-infrastructure/?utm_source=chatgpt.com)
* [Ground Truth — 对基础设施智能体和反馈循环的分析](https://groundtruth.day/news/z-ai-says-glm-helped-build-its-own-inference-infrastructure.html?utm_source=chatgpt.com)
* [Locsic — 推理栈的技术拆解](https://locsic.com/thinking/glm-inference-infrastructure/?utm_source=chatgpt.com)

[1]: https://gigazine.net/gsc_news/en/20260918-how-glm-built-inference-infrastructure/?utm_source=chatgpt.com "Z.ai 分享了使用中国制造的 AI 基础设施为‘GLM-5.3-Flash’提供生产服务的专业知识，展示了 AI 智能体如何管理基础设施，以实现与 NVIDIA GPU 相当的效率。- GIGAZINE"
[2]: https://www.techtwitter.com/tweet/05c8f469-b305-49dd-98c7-8bc9b519649f?utm_source=chatgpt.com "> 美国前沿实验室：‘RSI 即将来到我们身边’‘我们必须放慢’"
[3]: https://kokoknows.ai/article/link_external_linked_toward_recursive_self_improvement_how_glm_built_it?utm_source=chatgpt.com "走向递归式自我改进：GLM 如何构建自己的推理基础设施 — Koko Knows"
[4]: https://www.reddit.com/r/AIGuild/comments/1wjcfh8/glm53_helped_build_its_own_inference/?utm_source=chatgpt.com "GLM-5.3 帮助构建了自己的推理基础设施，并在两周内将吞吐量提高了两倍"
[5]: https://groundtruth.day/news/z-ai-says-glm-helped-build-its-own-inference-infrastructure.html?utm_source=chatgpt.com "Z.ai 表示 GLM 帮助构建了自己的推理基础设施 — Ground Truth"
