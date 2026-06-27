---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 添加论文的两个链接
translated: true
type: note
---

**问题：** 我是否应该将 GitHub 仓库链接（https://github.com/lzwjava/sec-edgar-gpt）和 Hugging Face 模型链接（https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf）加入论文（.tex）中？考虑到近期内容不会有太大变化——还是跳过论文，只把它们加在 Twitter 帖子中？

**答案：**

是的，把两个链接都放在论文里。这是正确的做法，理由很具体：

**论文是规范的存档制品，而推文是转瞬即逝的。** 六个月后，通过 arXiv、Google Scholar、引用或你的笔记网站找到你的 `.tex`/PDF 的人，需要能够*从文档本身*访问代码和权重。Twitter 帖子会衰退——一周后便难以搜索，如果账号变更则彻底失效，而且没人会引用一条推文。论文才是会被索引、转发和引用的内容。可复现性链接应当放在声明所在的地方。

**惯例强烈支持这样做。** 现代 ML 论文通常会在首页包含 `\footnote{Code: ...}` 并在末尾设置专门的复现性/制品章节。审稿人和读者期望看到“代码可获取于”和“权重可获取于”。一份 GPT-2 124M 复现论文如果没有仓库 + 检查点链接，说服力会大打折扣。

**“内容不会变化”这一点实际上*支持*添加链接，而非反对。** 稳定的链接正是存档文档所需要的。论文的风险在于链接到会腐烂变化的内容；既然你的仓库和 HF 模型是稳定的，论文链接就能保持有效。如果你担心未来变动，可以固定一个发布标签和特定的 HF 修订版本：

- `https://github.com/lzwjava/sec-edgar-gpt/tree/v1.0`
- `https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf/tree/<commit-sha>`

这样即使 `main` 分支有更新，论文指向的也是不可变的快照。

**在 `.tex` 中的具体位置：**

在标题页的第一页脚注（最显眼的位置）：

```latex
\title{SEC-EDGAR-GPT: ...%
\thanks{Code: \url{https://github.com/lzwjava/sec-edgar-gpt} \quad
Model: \url{https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf}}}
```

并在末尾添加一个简短的复现性章节：

```latex
\section{Code and Model Availability}
The training code, configuration, and dataset pipeline are released at
\url{https://github.com/lzwjava/sec-edgar-gpt}. Pretrained weights
(124M parameters, HF format) are available at
\url{https://huggingface.co/lzwjava/sec-edgar-gpt-124m-hf}.
```

确保你使用了 `\usepackage{hyperref}`（`url` 会被自动引入），这样 PDF 中的链接才是可点击的。

**两者都做——这不是二选一。** 论文 = 规范记录（必须包含链接）。Twitter = 分发/推广（为论文和仓库引流）。推文链接到论文；论文链接到制品。这才是正确的方向。交叉链接：GitHub README 也应链接到论文 PDF 和 HF 模型，这样每个入口点都能到达另外两个。

因此：现在就把两个链接加入 `.tex`，若想保持不可变性则固定到标签/修订版，然后在 Twitter 上发布并反向链接。