---
audio: false
generated: true
lang: zh
layout: post
title: Mistral AI的2025年模型上下文长度
translated: true
type: note
---

截至2025年6月，Mistral AI已发布多款具有不同上下文长度的模型。以下是部分关键模型及其上下文窗口的概要：

* **Magistral Small (magistral-small-2506)**：这款开放权重模型具备128k上下文窗口，但超过40k后性能可能下降，因此建议最大长度为4万个token
* **Magistral Medium (magistral-medium-2506)**：这款仅限API调用的推理模型同样建议使用40k上下文窗口
* **Mistral Small 3.1 (mistral-small-2503) / Mistral Small 3.2 (mistral-small-2506)**：这些模型的上下文窗口最高可达128,000个token
* **Codestral (codestral-2501)**：这款专注于代码生成的模型拥有256,000个token的大容量上下文窗口
* **Mistral Large 2 (mistral-large-2407 / mistral-large-2411)**：Mistral旗舰级大模型的上下文窗口为128k
* **Mistral NeMo (open-mistral-nemo-2407)**：这款与英伟达合作开发的120亿参数模型提供最高128,000个token的上下文窗口
* **Mistral Medium 3 (mistral-medium-2505)**：这款多模态模型同样支持128k上下文窗口

需特别注意，虽然部分模型宣称支持超大上下文窗口（如128k），但实际性能在稍小范围内（如Magistral系列的40k）可能更为优化。
