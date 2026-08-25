---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 检测非法特殊字符
translated: true
type: note
---

问题：NVIDIA Workday求职申请表实际上会检测哪些非法字符？其背后的检测规则是什么？

回答：系统拒绝你的"职位描述"文本是因为其中包含某些特殊字符。错误信息明确列出了以下字符：

`< > [ ] " { } \`

查看你的文本区域内容，最可能的触发字符是：

- `"`（直双引号）——你在"AI Full Stack Engineer"等引用短语中使用了它们
- `<` / `>` ——如果混入了任何Markdown风格的标签
- `\` ——可能出现在路径格式引用中

检测规则是一个简单的**字符黑名单**——通过服务端或客户端验证扫描原始文本中是否出现这八个字符，无论上下文如何。这并非专门针对HTML注入或SQL注入，而是Workday对自由文本字段应用的广泛净化过滤器，用于防止潜在的XSS（跨站脚本攻击）或模板注入攻击。只要字段中出现任何一个列出的字符，就会触发错误。

**修复方法：**

将违规字符替换为安全替代方案：

| 原字符 | 替换方案 |
| ---------- | ------------- |
| `"引用术语"` | 使用单引号 `'` 或直接删除引号 |
| `<` / `>` | 拼写为"小于"/"大于"，或直接删除 |
| `[链接]` 或 `[文本]` | 删除方括号 |
| `\路径\文件` | 改用 `/` |

由于你的描述中使用了"AI Full Stack Engineer"等双引号短语，只需切换为单引号或完全删除引号即可解决错误。

参考链接：

- [NVIDIA招聘网站——职位发布](https://nvidia.wd5.myworkdayjobs.com/en-US/NVIDIAExternalCareerSite/job/Senior-Platform-AI-Engineer---Silicon-Co-Design-Group_JR2016323)
