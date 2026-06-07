---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Python 3.11 安全删除
translated: true
type: note
---

分析：

---

**`/usr/local/bin/python3` (Python 3.11.6) — 可以安全删除**

该版本来自 python.org 安装程序（"Framework" 构建）。你还有：

- Homebrew 自带的 `python@3.11` (3.11.14) 位于 `/opt/homebrew/bin/python3.11`
- 所有 Homebrew 脚本的 shebang 指向 `/opt/homebrew/opt/python@3.11/...`，而非此路径
- 该目录下安装了 41 个 pip 包，但这些很可能与 Homebrew 或你的虚拟环境重复

官方卸载步骤：

```bash
# 1. 删除框架
sudo rm -rf /Library/Frameworks/Python.framework/Versions/3.11

# 2. 删除 /usr/local/bin 中的符号链接
sudo rm -f /usr/local/bin/python3.11 /usr/local/bin/python3
sudo rm -f /usr/local/bin/python3.11-config /usr/local/bin/python3-config
sudo rm -f /usr/local/bin/python3.11-intel64 /usr/local/bin/python3-intel64
sudo rm -f /usr/local/bin/pip3.11 /usr/local/bin/pip3
sudo rm -f /usr/local/bin/easy_install-3.11 /usr/local/bin/idle3.11
sudo rm -f /usr/local/bin/pydoc3.11 /usr/local/bin/2to3-3.11

# 3. 删除 Applications 文件夹
sudo rm -rf "/Applications/Python 3.11"
```

---

**`/usr/bin/python3` (Python 3.9.6) — 不要删除**

这是 **macOS 系统自带的 Python**，随 Xcode Command Line Tools 一起安装。它位于 SIP（系统完整性保护）下的 `/usr/bin/` 目录中，这意味着：

- macOS 会保护它——除非禁用 SIP，否则无法删除
- Xcode 和一些 Apple 开发工具依赖于它
- 它无害——位于 PATH 的最低优先级，不会与 Homebrew 冲突

请勿删除。
