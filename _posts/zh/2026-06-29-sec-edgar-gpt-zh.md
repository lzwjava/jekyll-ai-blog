---
audio: false
generated: false
image: true
lang: zh
layout: post
title: SEC-EDGAR-GPT：基于SEC文件训练的124M参数语言模型
translated: true
---

**免责声明：** 所有训练数据均公开于 Hugging Face。所有实验和训练均在我的个人设备或云平台上使用我的个人账户进行——未使用任何银行资源。

---

我用一块 RTX 4070 从零开始训练了一个 1.24 亿参数的 GPT-2 模型，训练数据来自 SEC-EDGAR 财务申报文件，共 15.5 亿 token。SEC-EDGAR 是美国证券交易委员会的公开公司申报数据库——包括 10-K 年报、10-Q 季报以及上市公司提交的其他披露文件。训练耗时约 8 小时，验证损失收敛至 2.28。

该模型能生成逼真的 SEC 标准用语——风险因素、管理层讨论与分析（MD&A）部分、业务描述——但在数值一致性和长程连贯性方面仍存在困难，这在当前规模下符合预期。

**代码：** [github.com/lzwjava/sec-edgar-gpt](https://github.com/lzwjava/sec-edgar-gpt) | **论文：** [sec-edgar-gpt.pdf](https://github.com/lzwjava/sec-edgar-gpt/raw/main/sec-edgar-gpt.pdf)

整个 1.24 亿参数模型——训练、部署、论文和网站——在 3 天内使用 Hermes Agent 完成。借助 AI 智能体，LLM 的研究与实践已变得真正触手可及。

感谢 Andrej Karpathy 的 nanoGPT 训练框架、Hugging Face 上的 kapilrao/SEC-EDGAR 数据集，以及 Ming Jian Wei、Du Chun 和 Parjanya Mudunuri 的有益讨论。

---

**关于我：** 我是一名在 GFT 工作的 AI 全栈工程师，通过合同安排与一家全球银行合作。过去一年中，我消耗了约 30 亿 LLM token，并在 RTX 4070、H200、B200 和 AMD MI300X 上训练了约 15 个小模型（最高 7.6 亿参数）。我在银行内部 GitHub 上贡献了 5000 多次，在公开 GitHub 上贡献了 11000 多次。我在该银行担任合同工程师已 2.5 年，分别在 WPB 和 GFT 工作。我曾向 80 位银行同事做过一场 AI 分享，交流实践经验。最近，我还与首席工程师 Parjanya Mudunuri 及我的主管 Ming Jian Wei 合作了约一个月，参与一个涉及大型 Excel 文件处理以及用于比较多个银行系统差距与差异的 join/union 工具项目。

正如银行 CEO 所言，AI 正成为我们这个时代最具定义性的技术之一。我希望这项工作能帮助银行在 AI 技术应用上更进一步。

---

**项目网站：**

![二维码：项目网站](assets/images/sec-edgar-gpt-workers-demo.png)

[sec-edgar-gpt.lzwjava.workers.dev](https://sec-edgar-gpt.lzwjava.workers.dev/)

![SEC-EDGAR-GPT 网站](assets/images/sec-edgar-gpt/website.png)

**聊天（试用模型）：**

![二维码：聊天](assets/images/sec-edgar-gpt/chat_qrcode.png)

[gq8kq409jjxh7r-8888.proxy.runpod.net](https://gq8kq409jjxh7r-8888.proxy.runpod.net/)

![SEC-EDGAR-GPT 聊天机器人](assets/images/sec-edgar-gpt/chatbot_web.png)

**HuggingFace 模型：**

![二维码：HuggingFace](assets/images/sec-edgar-gpt-huggingface.png)

[huggingface.co/lzwjava/sec-edgar-gpt-124m-hf](https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf)
