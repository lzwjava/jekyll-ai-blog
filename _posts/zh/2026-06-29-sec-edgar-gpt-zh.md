---
audio: false
generated: false
image: true
lang: zh
layout: post
title: SEC-EDGAR-GPT：一个基于SEC EDGAR申报文件从头训练的GPT-2 (124M)语言模型
translated: true
---

**免责声明：** 所有训练数据均已在 Hugging Face 上公开。所有实验和训练均在个人设备或云平台上使用个人账户完成——未使用任何银行资源。

---

我使用单张 RTX 4070，在 SEC-EDGAR 财务申报文件的 15.5 亿 tokens 上从头训练了一个 1.24 亿参数的 GPT-2 模型。SEC-EDGAR 是美国证券交易委员会的企业申报公开数据库——包含上市公司的 10-K 年报、10-Q 季报及其他披露文件。训练耗时约 8 小时，验证损失收敛至 2.28。

该模型能生成令人信服的 SEC 标准文本——风险因素、管理层讨论与分析（MD&A）章节、业务描述——但在数值一致性和长程连贯性方面存在困难，这在当前规模下属于预期表现。

**代码：** [github.com/lzwjava/sec-edgar-gpt](https://github.com/lzwjava/sec-edgar-gpt) | **论文：** [sec-edgar-gpt.pdf](https://github.com/lzwjava/sec-edgar-gpt/raw/main/sec-edgar-gpt.pdf)

整个 1.24 亿参数模型——包括训练、部署、论文和网站——均在 3 天内使用 Hermes Agent 完成。借助 AI 代理，LLM 研究和实践已真正变得触手可及。

感谢 Andrej Karpathy 的 nanoGPT 训练框架、Hugging Face 上的 kapilrao/SEC-EDGAR 数据集，以及 Ming Jian Wei、Du Chun 和 Parjanya Mudunuri 的有益讨论。

---

**关于我：** 我是一名 GFT 的全栈 AI 工程师，通过合同安排与一家全球银行合作。过去一年中，我处理了约 30 亿 LLM tokens，并在 RTX 4070、H200、B200 和 AMD MI300X 上训练了约 15 个小模型（最高 7.6 亿参数）。我在银行内部 GitHub 上贡献了 5000 多次，在公共 GitHub 上贡献了 11000 多次——借助 AI 工具并由人工审核验证。我在银行做了 2.5 年的合同工程师，包括 WPB 和 GFT 项目。我曾向 80 位银行同事发表 AI 演讲，分享实战经验。最近，我还与首席工程师 Parjanya Mudunuri 及我的主管 Ming Jian Wei 合作了一个月左右，参与了一个涉及大型 Excel 文件处理和联接/合并工具的项目，用于对比多个银行系统间的差异和差距。

正如银行 CEO 所言，AI 正成为我们这个时代的定义性技术之一。我希望这项工作能帮助银行更多地采用 AI 技术。

---

**项目网站（部署在 Cloudflare Workers，请使用个人设备访问）：**

![二维码：项目网站](assets/images/sec-edgar-gpt-workers-demo.png)

[sec-edgar-gpt.lzwjava.workers.dev](https://sec-edgar-gpt.lzwjava.workers.dev/)

![SEC-EDGAR-GPT 网站](assets/images/sec-edgar-gpt/website.png)

**聊天——试用模型（部署在 RunPod，请使用个人设备访问；$0.24/小时，数天后将关闭）：**

![二维码：聊天](assets/images/sec-edgar-gpt/chat_qrcode.png)

[gq8kq409jjxh7r-8888.proxy.runpod.net](https://gq8kq409jjxh7r-8888.proxy.runpod.net/)

![SEC-EDGAR-GPT 聊天机器人](assets/images/sec-edgar-gpt/chatbot_web.png)

**HuggingFace 模型：**

![二维码：HuggingFace](assets/images/sec-edgar-gpt-huggingface.png)

[huggingface.co/lzwjava/sec-edgar-gpt-124m-hf](https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf)