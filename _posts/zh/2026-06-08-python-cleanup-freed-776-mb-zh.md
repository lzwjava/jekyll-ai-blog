---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Python清理释放了776 MB
translated: true
type: note
---

## Python 清理总结

**开始状态：** 5 个 Python 安装
**结束状态：** 3 个 Python 安装（2 个 Homebrew + 1 个系统）

---

### 已移除

| 项目 | 版本 | 方式 | 释放空间 |
| ------ | --------- | ----- | ---------- |
| python.org 框架 | 3.11.6 | `sudo rm -rf /Library/Frameworks/Python.framework` + `/usr/local/bin` 中 14 个符号链接 + `/Applications/Python 3.11` | 约 200 MB |
| python@3.13 (Homebrew) | 3.13.12 | `brew uninstall`（删除 awscli/azure-cli 后自动作为孤立包移除） | 72 MB |
| awscli | 2.34.19 | `brew uninstall` | 154 MB |
| azure-cli | 2.84.0 | `brew uninstall` | 350 MB |

**总计释放空间：** 约 776 MB

---

### 剩余安装

| 路径 | 版本 | 角色 | 依赖项 |
| ------ | --------- | ------ | ---------------- |
| `/opt/homebrew/bin/python3` | 3.14.3 | **默认** (`python3`) | llvm, nmap, rust, yt-dlp, docutils + 85 个工具 |
| `/opt/homebrew/bin/python3.11` | 3.11.14 | ML 主力 | accelerate, ctranslate2, chroma, alembic + 75 个工具 |
| `/usr/bin/python3` | 3.9.6 | **macOS 系统** (Xcode CLT) | macOS 内部组件, Xcode — 无法移除 (SIP 保护) |

---

### 副作用

- 裸 `python3` 现在解析为 `/usr/bin/python3`（3.9.6）而非 Homebrew 的 3.14.3，因为你的 PATH 中 `/usr/bin` 排在 `/opt/homebrew/bin` 之前。之前 `/usr/local/bin` 中的旧 python.org 符号链接覆盖了此路径。修复方法：`ln -s /opt/homebrew/bin/python3 /usr/local/bin/python3`
- 旧 python@3.13 下的 464 个 pip 包和 20 个工具（ansible、ipython、markdown2 等）已全部消失。如需请重新安装到 python@3.14 下：`pip3 install ansible ipython markdown2`
