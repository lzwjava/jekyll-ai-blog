---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 重复笔记移除修复测试
translated: true
type: note
---

以下是发生的事情：

问题
=====
两篇笔记内容相同但文件名不同：
  - 2026-05-24-agentsmd-per-project-context-flow-en.md
  - 2026-05-24-how-hermes-agent-uses-project-context-files-en.md

重复检测测试（test_no_duplicate_notes）会在每个日期组内比较笔记正文内容。这两篇文件有完全相同的 79 行正文，内容是关于 AGENTS.md 在 Hermes Agent 中的工作方式（启动注入 + 运行时子目录提示）。

修复
=====
删除描述性较弱的重复文件（agentsmd-per-project-context-flow-en.md），保留命名更佳的文件（how-hermes-agent-uses-project-context-files-en.md）。

  git rm notes/2026-05-24-agentsmd-per-project-context-flow-en.md
  git commit -m "fix(notes): remove duplicate note, keep how-hermes-agent-uses-project-context-files-en"
  git push

CI 重新触发
=============
推送到 main 分支会自动触发 "Deploy Jekyll" 工作流（主部署流水线）。该工作流：
  1. 通过 DeepSeek 翻译文章/笔记
  2. 修复 markdown 表格
  3. 安装 ww CLI
  4. 运行单元测试（包括 test_no_duplicate_notes）← 现在应该能通过
  5. 构建 Jekyll 站点
  6. 部署到 lzwjava.github.io

"Build and Deploy" 工作流（手动触发）也运行了测试步骤。由于重复文件已删除，两者现在都应该通过。
