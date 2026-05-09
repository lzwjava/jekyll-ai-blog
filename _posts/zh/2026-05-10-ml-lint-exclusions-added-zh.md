---
audio: false
generated: true
image: false
lang: zh
layout: post
title: ML Lint排除添加汇总
translated: true
type: note
---

ml 排除规则生效——pre-commit 对所有 ml 文件均通过检查。存在 7 个预先存在的 pyright 失败，涉及无关模块（speech_to_text、audio、java_agent、try_tiktoken），原因为缺少可选依赖项（google-cloud-speech、pydub、jpype、tiktoken）——这些问题早于本次变更，且不在本次处理范围内。

差异摘要：

```toml
[tool.pyright]
exclude = [
    ".venv/",
    "ww/ml/",     # 新增
]

[tool.ruff]                      # 新增配置段
extend-exclude = ["ww/ml"]
```

`ww/ml/` 目录包含第三方学习/参考代码（Coursera、PyTorch 示例、Karpathy 项目）——其依赖项（torch、sklearn、scipy、pydub、plotly、dash）并非项目依赖，因此将其从两个 linter 中排除是合理做法。