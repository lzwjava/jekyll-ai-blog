---
audio: false
generated: true
image: false
lang: zh
layout: post
title: arXiv HTML 比 PDF 更优
translated: true
type: note
---

**问题：arXiv HTML 在阅读论文时是否比 PDF 更好，尤其是支持深色模式？**

**回答：是的，对于日常阅读，arXiv HTML 通常比 PDF 好得多。** 你提供的链接：

[https://arxiv.org/html/1706.03762v7](https://arxiv.org/html/1706.03762v7)

是 **"Attention Is All You Need"**（Transformer 论文）的 HTML 版本，它展示了为什么论文正在向网页原生格式迁移。arXiv 官方引入了 HTML 论文作为 PDF 之外的附加格式，以提高可访问性和阅读体验。([arXiv][1])

优点：

### 1. 深色模式

是的。HTML 遵循浏览器设置，因此如果你的操作系统/浏览器使用深色模式，论文可以自动以深色模式渲染。arXiv 的 HTML 设计专门支持外观变化，例如深色模式和字体调整。([Scribd][2])

示例：

```
浅色模式：
白色背景 + 黑色文字

深色模式：
深色背景 + 浅色文字
```

长时间阅读时对眼睛更友好。

---

### 2. 在笔记本电脑/手机上体验更好

PDF 是固定页面：

```
PDF：
+----------------+
| 论文页面       |
|                |
| 小字           |
|                |
+----------------+
```

HTML 是响应式的：

```
浏览器宽度
      |
      v

+----------------+
| Attention Is   |
| All You Need   |
|                |
| 文字自然流动   |
+----------------+
```

你可以：

* 调整字体大小
* 使用浏览器缩放
* 在手机上阅读
* 更轻松地复制公式/文字
* 在文档内搜索

这是 arXiv HTML 的主要动机之一。([Alexander Van Werde][3])

---

### 3. 更适合 AI 工作流

对于使用 LLM 的人来说，HTML 要好得多。

PDF：

```
paper.pdf
   |
   v
OCR / 解析器
   |
   v
有时公式损坏
```

HTML：

```
paper.html
   |
   v
结构化 DOM
   |
   +-- 标题
   +-- 公式
   +-- 参考文献
   +-- 图表
```

你可以直接：

* 将章节复制到 ChatGPT
* 抓取论文
* 构建 RAG 数据集
* 转换为 Markdown

许多 AI 论文工具现在在有条件时依赖 arXiv HTML。([GitHub][4])

---

### 4. 公式更美观

例如：

PDF：

```
Attention(Q,K,V)=softmax(QKᵀ/√dk)V
```

你可能需要放大。

HTML：

* 公式单独渲染
* 可随浏览器缩放
* 有时具有 MathML 可访问性

---

### 5. PDF 仍有优势

PDF 在以下方面仍然更好：

* 打印
* 精确页码引用
* 会议提交格式
* iPad 上的批注
* 归档

研究人员仍然使用 PDF，因为它是规范的“最终提交”格式。

---

我阅读 ML 论文的工作流：

```
首次阅读：
arxiv.org/html/xxxxx
        |
        |
        v
理解思路
记笔记

深入阅读：
下载 PDF
        |
        |
        v
检查精确公式
图表
附录
```

对于像：

* Attention Is All You Need
* FlashAttention
* GPT-3
* DeepSeek 论文
* LLaMA 论文

我现在会先阅读 HTML 版本。

参考资料：

* arXiv HTML 论文公告 ([arXiv][1])
* HTML 格式优势与深色模式讨论 ([Scribd][2])
* arXiv 可访问性更新 ([Vuink.com][5])

[1]: https://arxiv.org/abs/2402.08954?utm_source=chatgpt.com "HTML papers on arXiv -- why it is important, and how we made it happen"
[2]: https://www.scribd.com/document/882301275/2402-08954v1?utm_source=chatgpt.com "HTML Format for Accessible arXiv Papers | PDF | Te X | Html"
[3]: https://alexandervanwerde.be/applications-of-html-support-on-arxiv/?utm_source=chatgpt.com "HTML support on arXiv could be great! – Alexander Van Werde"
[4]: https://github.com/huggingface/skills/blob/main/skills/huggingface-papers/SKILL.md?utm_source=chatgpt.com "skills/skills/huggingface-papers/SKILL.md at main · huggingface/skills · GitHub"
[5]: https://vuink.com/post/oybt-d-dnekvi-d-dbet/2023/12/21/accessibility-update-arxiv-now-offers-papers-in-html-format?utm_source=chatgpt.com "Accessibility update: arXiv now offers papers in HTML format"