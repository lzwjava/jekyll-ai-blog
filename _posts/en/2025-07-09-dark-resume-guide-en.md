---
audio: false
generated: true
lang: en
layout: post
title: Create Dark Resume with LaTeX
translated: false
type: note
---

To support building a `resume-en-dark.pdf` using your `awesome-cv-dark.cls`, you'll need to:

### ✅ 1. Create a new LaTeX source file for the dark version

Duplicate your existing `resume-en.tex` into a new file that uses the dark theme class:

#### `latex/en/resume-en-dark.tex`

```latex
%-------------------------------------------------------------------------------
% CONFIGURATIONS
%-------------------------------------------------------------------------------
\documentclass[11pt, a4paper]{../awesome-cv-dark} % Use dark version here

% Configure page margins
\geometry{left=1.4cm, top=.8cm, right=1.4cm, bottom=1.8cm, footskip=.5cm}

% Color for highlights
\colorlet{awesome}{awesome-red}

% Set section highlight
\setbool{acvSectionColorHighlight}{true}

\usepackage{fontspec}
\usepackage{xeCJK}
\usepackage{ifthen}

% Include the actual resume content (same as your normal version)
\input{resume-en-content.tex}
```

> ✅ You can reuse your existing `resume-en-content.tex` to avoid duplication, or copy/paste from `resume-en.tex`.

---

### ✅ 2. Update the `Makefile`

Add a new rule in your `Makefile` for building `resume-en-dark.pdf`.

Find this part in the `Makefile`:

```make
latex: $(foreach x, coverletter coverletter-zh resume-zh resume, $x.pdf)
```

Modify it to include the dark resume:

```make
latex: $(foreach x, coverletter coverletter-zh resume-zh resume resume-en-dark, $x.pdf)
```

Then add the build rule:

```make
resume-en-dark.pdf: $(RESUME_EN_DIR)/resume-en-dark.tex $(RESUME_SRCS)
 $(CC) -output-directory=$(RESUME_EN_DIR) $<
```

> 🔁 If you keep all assets in the same folder (`latex/en/resume-en/`), you don’t need to update `RESUME_SRCS`.

---

### ✅ 3. Optional: Add to `copy` target

If you want to copy the generated file to `assets/resume`, update `copy`:

```make
 cp $(RESUME_EN_DIR)/resume-en-dark.pdf assets/resume/Zhiwei.Li.Resume.Dark.pdf
```

---

### ✅ 4. Build it

Now you can just run:

```bash
make resume-en-dark.pdf
```

---

Let me know if your content is shared across themes and you want a smarter structure using shared `.tex` files like `resume-en-content.tex`.
