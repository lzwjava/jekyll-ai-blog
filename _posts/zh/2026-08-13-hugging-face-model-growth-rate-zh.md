---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Hugging Face 模型增长率
translated: true
type: note
---

问题：Hugging Face 模型数量的增长速度有多快？真的能在 1-2 个月内增加约 100 万个模型吗？

答案：

是的，增长速度极快，但**“1-2 个月内增加 100 万个模型”的说法可能过高**，除非你计入某些异常峰值或仓库创建事件。实际的增长情况大致如下：

| 时间 | Hugging Face 公开模型数量 |
| ---------- | -----------------------: |
| 2024 年初 | 约 50万+ |
| 2025 年 1 月 | 约 127 万（[DOI][1]） |
| 2025 年 3 月 | 突破 **150 万**（[Hugging Face][2]） |
| 2025 年中 | 约 180 万（[Hugging Face][3]） |
| 2025 年底 | 突破 **200 万+**（[Hugging Face][4]） |

因此，大致增长率为：

```
2025 年 1 月：
127 万

2025 年 3 月：
150 万

增长：
+23 万 / 约 2 个月
≈ 11.5 万个模型/月
≈ 4000 个模型/天
```

2025 年后期：

```
150 万 → 200 万

+50 万个模型

历时数月
≈ 10 万-20 万/月
```

（[Hugging Face][4]）

感觉像爆炸式增长的原因是，Hugging Face 上的模型不再仅仅是“新的基础模型”。

很大一部分是：

```
基础模型
    |
    +-- LoRA 微调版本
    |
    +-- QLoRA 变体
    |
    +-- 合并后的检查点
    |
    +-- 量化 GGUF 版本
    |
    +-- 语言/领域适配版本
    |
    +-- 基准测试变体
```

示例：

```
meta-llama/Llama-3.1-8B
        |
        +-- 数千个社区版本
             |
             +-- 角色扮演
             +-- 编程
             +-- 中文
             +-- 医疗
             +-- 4-bit
             +-- 8-bit
             +-- 长上下文
             +-- 智能体调优
```

这创造了一种“AI GitHub 效应”：

* GitHub 拥有数百万个仓库，因为人们会 fork 并修改。
* Hugging Face 拥有数百万个模型，因为人们会微调并发布衍生版本。

生态系统正在从：

```
2018-2022：
“谁训练了最大的模型？”
```

转向：

```
2024-2026：
“谁为这个细分领域适配得最好？”
```

示例：

* 一个专为中文法律场景优化的 7B 模型
* 一个用于嵌入式设备的 3B 模型
* 一个用于工业检测的视觉模型
* 一个日英双语模型
* 一个编程智能体模型

这些小模型很有用，因为推理成本低。

值得关注的指标不仅仅是模型数量。分布是长尾的：

```
200 万个模型

前 0.01%
    主导下载量

绝大多数模型：
    下载量很少
    面向小众用户
    实验性质
```

Hugging Face 自身报告称，许多模型的使用率很低，而少数流行模型主导了下载量。([Hugging Face][4])

所以你的直觉是对的：

> Hugging Face 的多样性令人惊叹。有很多小型、奇特、专业的模型。

模型动物园正变得像一个生物生态系统：

```
Llama/Qwen/Mistral 基础模型
          |
          |
     数千个变体
          |
          |
 数百万个专业模型
```

“一个大模型 GPT 通吃一切”的时代可能正在走向一个拥有数百万个专业衍生模型的世界。([arxiv.org][5])

参考资料：

* Hugging Face 2026 年开源 AI 状态报告：([Hugging Face][4])
* Hugging Face 模型数量突破 150 万：([Hugging Face][2])
* Hugging Face 生态系统概览：([Hugging Face][3])
* 200 万 Hugging Face 模型解析：([arxiv.org][5])

[1]: https://doi.org/10.1145/3755881.3755921?utm_source=chatgpt.com "探索 Hugging Face 生态系统中的域名抢注威胁 | 第 16 届国际互联网软件会议论文集"
[2]: https://huggingface.co/posts/clem/238420842235482?utm_source=chatgpt.com "@clem 在 Hugging Face 上：“我们刚刚在 Hugging Face 上突破了 1,500,000 个公开模型（以及 50 万个 Spaces、33 万个…）”"
[3]: https://huggingface.co/blog/evijit/hf-hub-ecosystem-overview?utm_source=chatgpt.com "Hugging Face 社区在构建什么？"
[4]: https://huggingface.co/blog/huggingface/state-of-os-hf-spring-2026?utm_source=chatgpt.com "Hugging Face 开源状态：2026 年春季"
[5]: https://arxiv.org/abs/2508.06811?utm_source=chatgpt.com "机器学习生态系统解析：Hugging Face 上的 200 万个模型"
