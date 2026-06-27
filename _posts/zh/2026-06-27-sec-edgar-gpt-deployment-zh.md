---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SEC-EDGAR GPT 部署
translated: true
type: note
---

完成。已成功部署：<https://sec-edgar-gpt.lzwjava.workers.dev>

---

本次会话的所有更改摘要：

1. **.gitignore** — 添加了 LaTeX 中间文件（*.aux、*.log、*.out、*.toc、*.bbl、*.blg、*.fls、*.fdb_latexmk、*.synctex.gz、*.dvi）

2. **Git pull** — 从远程仓库拉取了最新内容（scripts/、server/、README 更新）

3. **论文（.tex）** — 在标题脚注中添加了 GitHub 仓库和 HuggingFace 模型链接，并新增了“代码与模型可用性”章节

4. **论文（.tex）** — 清理了图 2 的标题：移除了“训练损失曲线”前缀，保留了 Hermes Agent 提及

5. **已删除** paper1.png

6. **PDF 重新生成**（xelatex，2 次编译，19 页）

7. **网站** — 创建了 `website/index.html`，包含项目概述、关键数据、研究发现、引用和链接

8. **Cloudflare Worker** — 创建了 `wrangler.toml` 和 `src/index.js`，内嵌了 HTML（无需依赖）。修复了 Worker Sites 方法（env.ASSETS 在 Workers 中不可用），切换为自包含的内嵌 HTML

9. **HuggingFace 链接** — 将文本从“Model (HuggingFace)”改为“HuggingFace”

10. **已部署** 到 Cloudflare Workers，地址为 <https://sec-edgar-gpt.lzwjava.workers.dev>

所有更改已提交并推送到 GitHub。
