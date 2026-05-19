---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 固定液体原始标签
translated: true
type: note
---

所有23个文件已修复，现在每对 raw/endraw 标签都是平衡的。以下是摘要：

**修复了11个帖子主题中的23个文件**（每个主题包含英文和中文版本，以及DRY帖子）

问题：Jekyll的Liquid解析器在Markdown渲染之前运行，因此代码块（即使是围栏式 ``` 代码块）中的 `{{ }}` 和 `{% raw %}{% %}{% endraw %}` 会被解析为Liquid表达式。

修复方法：将每个受影响的围栏式代码块用 `{% raw %}...{% endraw %}` 包裹起来，这样Liquid就不会处理其中的内容：

- **Ansible帖子**（2个主题）：`{{ source_dir }}`、`{{ item.path | relpath(...) }}` 等
- **JSX帖子**：`{{ color: "red" }}` 样式对象  
- **Vault帖子**：Go模板 `{{.UserDN}}`
- **Angular帖子**（3个主题）：`{{ count() }}`、`{{ totalItems$ | async }}`
- **GitHub Actions帖子**：`{{ inputs.version || 'latest' }}`
- **Gitea Docker帖子**（2个主题）：`{{range $k,$v ...}}`、`{{.Names}}`
- **Nextcloud帖子**：`{{.Name}}`、`{{.CPUPerc}}`
- **DRY帖子**（英文+中文）：内联 `{% raw %}{% include %}{% endraw %}` 和 `{% raw %}{% include ... %}{% endraw %}` 分别用 `{% raw %}...{% endraw %}` 包裹