---
audio: false
generated: true
lang: zh
layout: post
title: 使用 LaTeX 制作暗色简历
translated: true
type: note
---

要使用 `awesome-cv-dark.cls` 构建 `resume-en-dark.pdf`，您需要：

### ✅ 1. 创建深色版本的 LaTeX 源文件

将现有的 `resume-en.tex` 复制为新文件，并改用深色主题类：

#### `latex/en/resume-en-dark.tex`

```latex
%-------------------------------------------------------------------------------
% 配置
%-------------------------------------------------------------------------------
\documentclass[11pt, a4paper]{../awesome-cv-dark} % 此处使用深色版本

% 配置页面边距
\geometry{left=1.4cm, top=.8cm, right=1.4cm, bottom=1.8cm, footskip=.5cm}

% 高亮颜色
\colorlet{awesome}{awesome-red}

% 设置章节高亮
\setbool{acvSectionColorHighlight}{true}

\usepackage{fontspec}
\usepackage{xeCJK}
\usepackage{ifthen}

% 包含实际简历内容（与常规版本相同）
\input{resume-en-content.tex}
```

> ✅ 您可以复用现有的 `resume-en-content.tex` 避免重复，或从 `resume-en.tex` 复制内容。

---

### ✅ 2. 更新 `Makefile`

在 `Makefile` 中添加构建 `resume-en-dark.pdf` 的新规则。

找到 `Makefile` 中的这部分：

```make
latex: $(foreach x, coverletter coverletter-zh resume-zh resume, $x.pdf)
```

修改为包含深色简历：

```make
latex: $(foreach x, coverletter coverletter-zh resume-zh resume resume-en-dark, $x.pdf)
```

然后添加构建规则：

```make
resume-en-dark.pdf: $(RESUME_EN_DIR)/resume-en-dark.tex $(RESUME_SRCS)
	$(CC) -output-directory=$(RESUME_EN_DIR) $<
```

> 🔁 如果所有资源都在同一文件夹（`latex/en/resume-en/`）中，则无需更新 `RESUME_SRCS`。

---

### ✅ 3. 可选：添加到 `copy` 目标

如果希望将生成的文件复制到 `assets/resume`，更新 `copy`：

```make
	cp $(RESUME_EN_DIR)/resume-en-dark.pdf assets/resume/Zhiwei.Li.Resume.Dark.pdf
```

---

### ✅ 4. 构建

现在只需运行：

```bash
make resume-en-dark.pdf
```

---

如果您的内容在多个主题间共享，并希望使用像 `resume-en-content.tex` 这样的共享 `.tex` 文件实现更智能的结构，请告知我。
