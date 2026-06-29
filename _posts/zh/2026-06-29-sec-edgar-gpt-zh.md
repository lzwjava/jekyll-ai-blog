---
audio: false
generated: false
image: true
lang: zh
layout: post
title: SEC-EDGAR-GPT：一个基于SEC文件训练的124M参数语言模型
translated: true
---

**免责声明：** 所有训练数据均来自 Hugging Face 公开数据集。所有实验和训练均使用我个人设备或云平台上的个人账户完成——未使用任何银行资源。

---

我使用单张 RTX 4070，在 SEC-EDGAR 财务申报文件的 15.5 亿 token 上从头训练了一个 1.24 亿参数的 GPT-2 模型。SEC-EDGAR 是美国证券交易委员会的上市公司申报文件公开数据库——包括 10-K 年报、10-Q 季报及其他披露文件。训练耗时约 8 小时，验证损失收敛至 2.28。

该模型能生成逼真的 SEC 标准文本——风险因素、管理层讨论与分析（MD&A）章节、业务描述——但在数值一致性和长程连贯性方面存在不足，这在此规模下属于预期表现。

**代码：** [github.com/lzwjava/sec-edgar-gpt](https://github.com/lzwjava/sec-edgar-gpt) | **论文：** [sec-edgar-gpt.pdf](https://github.com/lzwjava/sec-edgar-gpt/raw/main/sec-edgar-gpt.pdf)

整个 1.24 亿参数模型——包括训练、部署、论文和网站——均在 3 天内使用 Hermes Agent 完成。借助 AI 智能体，LLM 研究与实践已变得真正触手可及。

感谢 Andrej Karpathy 的 nanoGPT 训练框架、Hugging Face 上的 kapilrao/SEC-EDGAR 数据集，以及 Ming Jian Wei、Du Chun 和 Parjanya Mudunuri 的有益讨论。

---

**关于我：** 我是 GFT 的一名合同工程师，服务于一家全球性银行。过去一年中，我处理了约 30 亿 LLM token，并在 RTX 4070、H200、B200 和 AMD MI300X 上训练了约 15 个小模型（最大 7.6 亿参数）。我在银行内部 GitHub 上贡献了 5000 多次，在公共 GitHub 上贡献了 11000 多次。我在该银行担任合同工程师已有 2.5 年，先后在 WPB 和 GFT 部门工作。我曾为 80 位银行同事举办 AI 讲座，分享实践经验。最近，我还与首席工程师 Parjanya Mudunuri 及我的主管 Ming Jian Wei 合作约一个月，参与一个涉及大型 Excel 文件处理及跨多个银行系统差异对比的 join/union 工具项目。

正如银行 CEO 所言，AI 正成为我们这个时代最具定义性的技术之一。我希望这项工作能帮助银行更好地采用 AI 技术。

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