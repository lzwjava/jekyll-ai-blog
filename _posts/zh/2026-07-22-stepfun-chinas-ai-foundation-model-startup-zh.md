---
audio: false
generated: true
image: false
lang: zh
layout: post
title: StepFun：中国AI基础模型初创公司
translated: true
type: note
---

问题：**StepFun**简介（[https://www.stepfun.com/](https://www.stepfun.com/)）

答案：

## 概述

StepFun（中文名：上海阶跃星辰智能科技有限公司）是中国领先的基础模型初创公司之一，常与月之暗面（Moonshot AI）、MiniMax、智谱AI等公司并称为中国新一代前沿AI实验室。公司成立于**2023年4月**，总部位于**上海**。（[维基百科][1]）

公司正在构建：

* 大语言模型（LLM）
* 多模态模型（视觉+语言）
* 语音模型（ASR/TTS）
* 图像生成/编辑模型
* 面向智能体的模型
* 面向开发者的API平台

其当前定位类似于OpenAI或Anthropic提供的服务，但专注于中国市场并日益面向国际开发者。

---

## 创始人

公司由前微软高管创立：

* 姜大昕（CEO）
* 朱一博
* 焦斌星

姜大昕此前担任微软副总裁，拥有深厚的系统/软件工程背景。（[维基百科][1]）

---

## 融资

StepFun吸引了中国主要投资者，包括：

* 腾讯
* 启明创投
* 上海国资背景的投资基金

根据近期报道，该公司已完成多轮大额融资，并正在筹备香港IPO，估值据称约为**100–120亿美元**。（[维基百科][1]）

---

## 模型家族

StepFun开发了多个模型系列。

### Step 3.x

其旗舰LLM系列。

近期发布包括：

* Step 3
* Step 3.5 Flash
* Step 3.7 Flash

这些模型强调：

* 编程
* 智能体
* 工具使用
* 长上下文
* 多模态推理

其官方平台将Step 3.7 Flash描述为针对生产级智能体优化，具备可靠的工具编排、浏览器/终端交互、MCP兼容性以及多模态理解能力。（[StepFun][2]）

---

### Step-Audio

中国较为强大的开源语音模型之一。

能力包括：

* 语音识别
* 语音合成
* 声音克隆
* 情感控制
* 多语言语音

他们还发布了研究论文并开源了部分系统。（[arXiv][3]）

---

### Step Image

图像生成和编辑模型，旨在与FLUX、GPT Image、Midjourney等系统在开发者工作流中竞争。（[StepFun][2]）

---

### 智能体模型

一个重要的战略方向。

近期产品包括：

* Step DeepResearch
* Step Plan
* 面向智能体的Flash模型

公司正在大力投入：

* 浏览器智能体
* 编程智能体
* 工具调用
* 规划
* 长周期推理

而非仅限聊天机器人式的交互。（[StepFun][4]）

---

## 研究

与许多主要提供API的初创公司相比，StepFun发表了大量研究成果。

例如：

* Step-3系统/模型协同设计
* Step-Audio
* Step-Prover
* Step-Formalizer

主题包括：

* 高效推理
* 定理证明
* 语音模型
* 强化学习
* 多模态学习
* 推理
* 智能体系统

（[arXiv][5]）

---

## 开源

他们已开始开源多个项目，包括：

* Step-Audio
* StepDeepResearch
* 部分版本的模型检查点

近期发布的Step 3.7 Flash提供BF16、FP8和GGUF等格式，支持本地推理。（[Reddit][6]）

---

## 开发者平台

其API平台提供：

* 聊天补全API
* 视觉API
* 图像API
* 语音API
* 嵌入向量
* 面向智能体的模型
* 订阅计划（"Step Plan"）

该平台面向使用Cursor、Claude Code、OpenClaw及其他智能体框架进行开发的开发者。（[StepFun][2]）

---

## 为什么StepFun值得关注

从工程角度来看，StepFun之所以有趣，是因为它同时聚焦于多个前沿领域：

* 生产级智能体模型
* 多模态推理
* 高效MoE架构
* 模型-系统协同设计以实现更快推理
* 开源语音技术
* 长上下文编程模型

如果你对LLM基础设施、推理优化或智能体工程感兴趣，StepFun是除了DeepSeek和月之暗面之外值得关注的中国实验室之一。

参考文献：

* [StepFun官网](https://www.stepfun.com/?utm_source=chatgpt.com)
* [StepFun开放平台](https://platform.stepfun.ai/?utm_source=chatgpt.com)
* [开发者文档](https://platform.stepfun.ai/docs/en/step-plan/overview?utm_source=chatgpt.com)

[1]: https://en.wikipedia.org/wiki/StepFun?utm_source=chatgpt.com "StepFun"
[2]: https://platform.stepfun.ai/?utm_source=chatgpt.com "StepFun开放平台"
[3]: https://arxiv.org/abs/2502.11946?utm_source=chatgpt.com "Step-Audio：统一理解与生成的智能语音交互"
[4]: https://platform.stepfun.ai/docs/en/step-plan/overview?utm_source=chatgpt.com "Step Plan概述 - StepFun文档"
[5]: https://arxiv.org/abs/2507.19427?utm_source=chatgpt.com "Step-3：大而实惠——模型-系统协同设计实现低成本解码"
[6]: https://www.reddit.com/r/LocalLLM/comments/1trlnrp/stepfun_releases_step_37_flash_a_198b_moe/?utm_source=chatgpt.com "StepFun发布Step 3.7 Flash：一个198B MoE视觉语言模型，用于编程智能体和搜索工作流"
