---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 李卓翰：vLLM 联合创始人
translated: true
type: note
---

**问题：** vLLM 中的李卓涵（Zhuohan Li）是谁？

**回答：**

李卓涵（GitHub：`zhuohan123`）是 **vLLM 的共同创建者**，与 Woosuk Kwon 拥有同等的创始地位。以下是完整情况：

**起源故事：** 2022 年夏天，李卓涵与研究伙伴 Woosuk Kwon 试图通过跨 GPU 分配工作来提升大型深度学习模型的效率。当他们搭建演示时，性能表现极差。李卓涵表示："我们意识到内存管理将成为服务这些模型的重大瓶颈。" 在接下来的几个月里，李卓涵与 Kwon 深入钻研，最终从经典虚拟内存和分页技术中获得灵感，开发出了 PagedAttention。

**背景：** 李卓涵是加州大学伯克利分校的计算机科学博士生，师从 Ion Stoica，专注于高效机器学习系统——特别是大型模型的训练与部署。他的研究作品包括 Alpa、AlpaServe、Vicuna 以及 vLLM（PagedAttention）。他本科毕业于北京大学，并在微软研究院、Anyscale 和 Google Brain 实习过。

**博士论文：** 他 2024 年在伯克利完成的博士论文《以大模型赋能高效自动化系统》涵盖了 AlpaServe（用于扩展服务规模的模型并行技术）以及 vLLM/PagedAttention（内存利用与推理吞吐量优化）。

**曾在 OpenAI 工作，现就职于 Meta：** 在构建 vLLM 之后，李卓涵加入了 OpenAI，负责为 GPT-OSS 落地的基础设施和推理工作。他目前在 Meta 继续构建 vLLM。

**一句话总结：** 李卓涵是 **vLLM 的中国联合创始人**（北京大学本科 → 师从 Ion Stoica 的伯克利博士），与 Woosuk Kwon 共同发明了 PagedAttention，随后加入 OpenAI，目前正在 Meta 继续 vLLM 的相关工作。他在 GitHub/X 平台上的账号是 `zhuohan123`。