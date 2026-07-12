---
audio: false
generated: true
image: false
lang: zh
layout: post
title: TRAE在中国无法使用
translated: true
type: note
---

问题：为什么 TRAE Work 在我的地区（广州/中国大陆）显示“工作不可用”？

回答：

这里叠加了两个独立的问题，了解它们很有必要，因为你在其他 AI 开发工具上也会遇到类似情况。

**1. TRAE 严格区分国内版和国际版**

字节跳动将 TRAE 作为两个独立产品运营，分属不同实体：

- `trae.ai` — 国际版，面向海外用户，基于 GPT/Claude 模型
- `trae.com.cn` — 中国大陆国内版，使用 DeepSeek-R1 及其他国内模型

如果你从中国大陆 IP 访问 `trae.ai`（或其“TRAE Work”团队产品），会遭到屏蔽或降级处理——在中国使用海外版 Trae 会导致登录和连接问题（网络拥堵），大多数人的解决方法是使用 VPN，或者直接切换到国内版 Trae.com.cn（全中文界面）。具体到“TRAE Work”，它是国际版中较新的 B2B/团队层级产品，因此比基础 IDE 更可能严格按 IP/账单地区进行地理围栏。

**2. 底层模型访问也在收紧**

除了字节跳动自身的地理围栏，还有第二个问题：TRAE 海外版是 Anthropic 和 OpenAI 模型的下游转售商。Anthropic 已宣布将收紧对总部位于中国等不支持地区、且由这些地区公司持股超过 50% 的实体的访问限制——无论该实体实际位于何处。而 Trae 作为字节跳动为海外用户打造的 AI 代码编辑器，已知使用了 GPT 和 Claude 模型，这让担心失去 Claude 访问权限的用户感到不安。因此，即使你个人身处何地，一个完全“国际版”的 TRAE 产品（归字节跳动所有）也面临上游模型访问被切断的风险，这与你的地理位置无关。

**这对你的配置意味着什么**

既然你正在做国际咨询并构建代理工具，我不建议将 TRAE Work 作为关键基础设施——它处于两条不同监管红线的交汇处（中国出境限制 + 美国模型提供商入境限制），这种依赖关系无论你当下怎么做，都可能在一夜之间消失。如果你想要一个字节跳动模型级别的编码代理且不受地区抽签影响，`trae.com.cn`（基于 DeepSeek-R1）在地理上对你来说是稳定的。如果你特别想要基于 Claude/GPT 的代理式编码，那么你自己的 CLI 代理（`ww`、`iclaw`、`zz`）通过 OpenRouter 或直接调用 API 密钥，可以完全避开这类问题——你已经拥有基础设施，无需依赖转售商的地理围栏决策。

参考资料：

- [支持的国家和地区 - TRAE 文档](https://docs.trae.ai/ide/supported-countries-and-regions)
- [为什么 Trae 在中国无法使用以及如何修复？ - AI 分享圈](https://aisharenet.com/en/trae-guoneiweishenme/)
- [科技战：Anthropic 的 Claude 限制使中国支持的海外 AI 工具陷入困境 - 南华早报](https://www.scmp.com/tech/tech-war/article/3324583/tech-war-anthropics-claude-restrictions-put-overseas-ai-tools-backed-china-limbo)