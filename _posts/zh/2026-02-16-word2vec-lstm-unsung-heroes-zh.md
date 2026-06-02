---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Word2Vec 与 LSTM 的幕后英雄
translated: true
type: note
---

Question: Who are the main authors of Word2Vec and LSTM, and do they receive enough credit compared to figures like Yann LeCun?

Answer:

**Word2Vec** 技术主要由 **Tomáš Mikolov**（第一作者）以及共同作者 Kai Chen、Greg Corrado、Ilya Sutskever 和 Jeff Dean 在 Google 开发。它在 2013 年的两篇关键论文中被引入：一篇关于 word representations 的高效估算，另一篇关于词与短语的 distributed representations。Mikolov 被广泛公认为 Word2Vec 的主要创造者和核心推动者，该技术通过实现能够捕捉语义关系的高质量快速度 word embeddings（例如著名的向量算术 "king - man + woman ≈ queen"），在 NLP 领域产生了巨大影响。

**LSTM** (Long Short-Term Memory) 由 **Sepp Hochreiter** 和 **Jürgen Schmidhuber** 发明。他们 1997 年发表在 Neural Computation 上的开创性论文引入了这种架构，以解决 recurrent neural networks 中的 vanishing gradient problem，使模型能够有效地学习 long-range dependencies。这项工作为 sequence modeling 奠定了关键基础，在 transformer 占据主导地位之前，LSTM 驱动了语音识别、machine translation 等领域的诸多进步。

**Yann LeCun** 是 convolutional neural networks (**CNNs**) 的先驱，其主要贡献始于 20 世纪 80 年代末/90 年代初（例如用于手写识别的 LeNet）。他因在深度学习领域的整体贡献，与 Geoffrey Hinton 和 Yoshua Bengio 共同获得了 2018 年的图灵奖。

关于荣誉分配的观点在 AI 社区中确实经常被讨论：

- 像 LeCun、Hinton 和 Bengio 这样的人物获得了极高的公众认可（图灵奖、被媒体称为“深度学习教父”）、高知名度的职位（如 LeCun 在 Meta）以及广泛的赞誉。
- 相比之下，Mikolov 的 Word2Vec 是现代 NLP 中引用率最高且实际应用最广的创新之一，但他在主流 AI 叙事中的可见度较低。
- Hochreiter 和 Schmidhuber 做出了基础性的贡献（LSTM 极具影响力，1997 年的论文是深度学习历史上引用次数最多的论文之一），但 Schmidhuber 尤其经常表达不满，认为尽管在 RNNs、LSTMs 等领域拥有优先权，但相对于“三巨头”（Hinton, LeCun, Bengio）获得的荣誉较少。

许多研究者都有类似的感受：那些默默构建基础工具并公开成果（通常在当时没有激进的自我宣传或强大的企业后台支持）的人往往成为“幕后英雄”。他们的工作是免费提供的，并为无数应用和公司提供动力，但财务和名声的回报往往不成比例地流向了那些拥有更高知名度、更好时机或更强机构支持的人。

尽管如此，在研究社区内部，Mikolov、Hochreiter 和 Schmidhuber 受到了高度尊重和引用。即便聚光灯有时转向别处，Word2Vec 和 LSTM 已经以非常切实的方式改变了 AI。

References:

- [Word2vec - Wikipedia](https://en.wikipedia.org/wiki/Word2vec)
- [Efficient Estimation of Word Representations in Vector Space (arXiv)](https://arxiv.org/abs/1301.3781)
- [Long short-term memory - Wikipedia](https://en.wikipedia.org/wiki/Long_short-term_memory)
- [Long Short-Term Memory (original 1997 paper)](https://www.bioinf.jku.at/publications/older/2604.pdf)
