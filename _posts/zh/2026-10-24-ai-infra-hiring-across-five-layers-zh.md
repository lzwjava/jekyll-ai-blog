---
audio: false
generated: true
image: false
lang: zh
layout: post
title: AI基础设施招聘的五个层面
translated: true
type: note
---

**问题:** 哪些类型的公司招聘AI基础设施角色，为什么——仅仅是前沿实验室吗？

**答案:**

绝对不仅仅是前沿实验室。AI基础设施招聘现在至少分布在堆栈的**五个不同层面**：

---

### 1. 前沿实验室（OpenAI、Anthropic、xAI、Mistral、DeepMind）

这些是角色的起源——构建GPU集群、分布式训练系统和低层推理优化。前沿实验室如OpenAI、Anthropic、xAI和Mistral不再仅仅是模型公司；它们正在成为基础设施企业。他们的基础设施工程师处理集群编排、CUDA级调优和容错训练运行。

---

### 2. 超大规模提供商（AWS、Google Cloud、Microsoft Azure）

四个科技巨头预计在2026年在AI基础设施上花费约7250亿美元，这个金额超过除二十个国家外所有国家的GDP。为了吸收这些资本支出，他们需要基础设施工程师来构建和运营GPU数据中心、定制AI芯片（TPU、Trainium等）以及模型服务平台。例如，Amazon宣布计划招聘11,000名软件开发者和工程师以支持AWS运营——这是针对技能的调整而非总体增长。

---

### 3. GPU云 / 计算提供商

像Together AI、Modal、Lambda Labs和Crusoe这样的公司处于超大规模提供商和最终用户之间。Modal筹集了3.55亿美元用于无服务器GPU基础设施，Together AI在旧金山和阿姆斯特丹都有开放的AI基础设施工程师职位。他们需要工程师来构建高效的多租户GPU调度、自动伸缩和成本优化系统。

---

### 4. AI工具与平台公司

向量数据库（Pinecone、Weaviate）、MLOps平台和评估框架都需要基础设施工程师来使他们的产品可扩展。这些工具公司招聘后端和基础设施工程师、开发者关系人员和技术写作者。

---

### 5. 国防、医疗、金融与企业

特别是在EMEA地区，银行、国防主承包商和关键基础设施运营商越来越不信任美国托管的AI用于他们最敏感的工作流程——这推动了对本地或主权AI基础设施的需求。Anduril、Shield AI和Palantir都出现在职位列表中。还有一些临床AI初创公司招聘高级工程师来构建可扩展的后端和ML基础设施。

---

### 为什么他们都这样做？

根本原因在2024–2025年左右发生了转变。AI人才瓶颈不再在模型训练——而是在将AI扩展、部署和集成到生产系统中。具体来说：

- **训练规模：** 跨数千个GPU的分布式训练需要专门的系统工程师。
- **推理优化：** 以低成本大规模服务模型（vLLM、TensorRT-LLM）是一个困难的基础设施问题。
- **生产可靠性：** ML系统中的SLA、容错和可观测性不同于经典的软件工程基础设施。
- **数据管道与评估：** LLMOps工程师需要GPU级调优、Ray编排以及深度理解延迟敏感推理——普通DevOps背景不足以胜任。
- **成本控制：** GPU时间昂贵；能削减20%计算成本的基础设施工程师可以节省数百万美元。

目前，仅AI初创公司就有630个开放的MLOps/基础设施工程师职位，分布在265家AI初创公司中，其中39%在早期公司（种子前到B轮）——所以需求确实广泛，而不只是集中在前沿。

---

**参考：**

- [The AI Companies Quietly Hiring Beyond OpenAI and Nvidia](https://www.metaintro.com/blog/ai-companies-hiring-beyond-openai-nvidia-2026)
- [MLOps / Infrastructure Engineer Jobs at AI Startups](https://www.fastaijobs.com/jobs/role/mlops-infra-engineer)
- [AI Infrastructure Staffing: Building Teams for the AI Compute Boom](https://www.kore1.com/category/ai/page/7/)
- [AI Careers in 2025+](https://modelcraft.substack.com/p/ai-careers-in-2025)
- [Portability-First AI Strategy for Mid-Market CTOs](https://baytechconsulting.com/blog/portability-first-ai-strategy-mid-market-ctos-cfos-2026)
