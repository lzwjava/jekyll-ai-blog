---
audio: false
generated: false
image: false
lang: zh
layout: post
title: 使用 Awesome-CV 生成专业简历
translated: true
type: post
---

### 介绍

在使用 [ZhiyeApp](https://www.zhiyeapp.com) 之前，我转向了功能强大且高度可定制的 [Awesome-CV](https://github.com/posquit0/Awesome-CV)。这个基于 LaTeX 的模板使得创建专业简历变得简单且可高度定制。

---

### 为什么选择 Awesome-CV？

- 可定制：您可以个性化设置部分内容、颜色和格式。
- 专业外观：简洁的设计，完美适用于求职申请。
- 易于使用：只需最基本的 LaTeX 知识即可操作。

---

### 我的简历示例

以下是我使用的 `resume.tex` 文件的简化版本：

```latex
%-------------------------------------------------------------------------------
% 配置
%-------------------------------------------------------------------------------
\documentclass[11pt, a4paper]{awesome-cv}

% 页面边距和部分高亮
\geometry{left=1.4cm, top=.8cm, right=1.4cm, bottom=1.8cm, footskip=.5cm}
\colorlet{awesome}{awesome-red}
\setbool{acvSectionColorHighlight}{true}

%-------------------------------------------------------------------------------
% 个人信息
%-------------------------------------------------------------------------------
\name{Zhiwei}{Li}
\position{全栈工程师{\enskip\cdotp\enskip}后端工程师}
\address{中国广州}
\mobile{(+86) 132-6163-0925}
\email{lzwjava@gmail.com}
\homepage{https://lzwjava.github.io}
\github{lzwjava}
\linkedin{lzwjava}
\quote{``自由与真理"}

%-------------------------------------------------------------------------------
\begin{document}

% 页头和页脚
\makecvheader[C]
\makecvfooter{\today}{Zhiwei Li~~~·~~~简历}{\thepage}

% 内容部分
\input{resume/summary.tex}
\input{resume/experience.tex}
\input{resume/education.tex}
\input{resume/corporateprojects.tex}
\input{resume/personalprojects.tex}
\input{resume/blogposts.tex}
\input{resume/papers.tex}
\input{resume/books.tex}
\input{resume/skills.tex}
\input{resume/tools.tex}
\input{resume/knowledge.tex}
\input{resume/certificates.tex}

\end{document}

自动化 Makefile

为了自动化 PDF 生成过程，我使用了以下的 Makefile：

```Makefile
.PHONY: awesome-cv

CC = xelatex
EXAMPLES_DIR = awesome-cv
RESUME_DIR = awesome-cv/resume
RESUME_ZH_DIR = awesome-cv/resume-zh
RESUME_SRCS = $(shell find $(RESUME_DIR) -name '*.tex')
RESUME_ZH_SRCS = $(shell find $(RESUME_ZH_DIR) -name '*.tex')

awesome-cv: $(foreach x, coverletter resume-zh resume, $x.pdf)

resume.pdf: $(EXAMPLES_DIR)/resume.tex $(RESUME_SRCS)
 $(CC) -output-directory=$(EXAMPLES_DIR) $<

resume-zh.pdf: $(EXAMPLES_DIR)/resume-zh.tex $(RESUME_ZH_SRCS)
 $(CC) -output-directory=$(EXAMPLES_DIR) $<

coverletter.pdf: $(EXAMPLES_DIR)/coverletter.tex
 $(CC) -output-directory=$(EXAMPLES_DIR) $<

clean:
 rm -rf $(EXAMPLES_DIR)/*.pdf
```

### 工作原理

1. 运行 `make awesome-cv` 生成以下 PDF 文件：
   • `resume.pdf`：英文简历
   • `resume-zh.pdf`：中文简历
   • `coverletter.pdf`：求职信

2. 运行 `make clean` 删除所有生成的 PDF 文件。

### 结论

通过利用 Awesome-CV 和这个 Makefile 配置，生成和维护专业简历变得轻松无比。无论是申请技术职位还是分享您的成就，Awesome-CV 都能帮助您美观且高效地展示自己的工作。

更多详情请访问 Awesome-CV 的 GitHub 仓库：[Awesome-CV on GitHub](https://github.com/posquit0/Awesome-CV)。
