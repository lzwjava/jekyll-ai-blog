---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 移除具有错误 shebang 的废弃二进制文件
translated: true
type: note
---

已删除。`pi` 已被移除——无论是二进制文件还是包文件。

**根因回顾：**

- `pi` 是一个 Python 2 包（2013 年，已废弃），通过 pip 安装在一个 Python 3.13 环境下，而该环境在此机器上已不存在
- Shebang 行 `#!/usr/bin/python3.13` → "找不到所需文件"
- 该包本身与 Python 3 完全不相容（使用了 `print` 语句语法、已弃用的 `imp` 模块）

如果你需要审计 `~/.local/bin/` 中其他失效的二进制文件：

```
file ~/.local/bin/* | grep -E "Python script" | while read f _; do
  head -1 "$f" | grep -q "$(python3 --version 2>&1 | cut -d' ' -f2 | cut -d. -f1-2)" || echo "无效 SHEBANG: $f"
done
```
