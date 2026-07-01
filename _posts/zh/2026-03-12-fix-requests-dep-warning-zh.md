---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 快速修复 Requests 依赖警告
translated: true
type: note
---

Question: 如何修复关于 urllib3 或 chardet/charset_normalizer 不匹配支持版本的 `RequestsDependencyWarning`？

Answer:

## 理解警告

此警告表示已安装的 `urllib3`、`chardet` 或 `charset_normalizer` 版本与您的 Python 环境（`/opt/homebrew/lib/python3.14`）中安装的 `requests` 版本**不兼容**。它**不会**破坏功能，但表示版本不匹配。

---

## 修复选项（按顺序尝试最佳）

### ✅ 选项 1 — 一起升级所有三个包（推荐）

这是最可靠的修复方法。将 `requests`、`urllib3` 和 `charset-normalizer` 升级到相互兼容的版本：

```bash
pip3.14 install --upgrade requests urllib3 charset-normalizer
```

由于您使用的是带有 Homebrew 的 macOS Python，您可能需要：

```bash
pip3 install --upgrade requests urllib3 charset-normalizer
```

---

### ✅ 选项 2 — 干净地重新安装 `requests`

有时全新重新安装可以自动解决依赖解析问题：

```bash
pip3 install --force-reinstall requests
```

---

### ✅ 选项 3 — 使用虚拟环境（最佳实践）

由于您的路径是 `/opt/homebrew/lib/python3.14`，您正在全局安装包到 Homebrew Python 中。这经常与其他工具引起版本冲突。使用虚拟环境可以隔离您的项目：

```bash
python3.14 -m venv myenv
source myenv/bin/activate
pip install requests urllib3 charset-normalizer
```

---

### ✅ 选项 4 — 抑制警告（快速变通方法）

如果您只想静默它而不修复根本原因，请在 Python 脚本顶部添加以下内容：

```python
import warnings
from requests import packages
warnings.filterwarnings('ignore', category=packages.urllib3.exceptions.RequestsDependencyWarning)
```

或者使用以下命令运行脚本：

```bash
python3 -W ignore::Warning your_script.py
```

---

### ✅ 选项 5 — 检查当前版本并找出冲突

运行以下命令查看确切安装的内容：

```bash
pip3 show requests urllib3 chardet charset-normalizer
```

然后查看 [requests 的 PyPI 页面](https://pypi.org/project/requests/)，了解您安装的 `requests` 版本所需 `urllib3` 和 `charset-normalizer` 的版本，并相应调整。

---

## 根本原因总结

| 包 | 作用 |
| --- | --- |
| `requests` | HTTP 库 — 依赖 urllib3 和字符集检测 |
| `urllib3` | requests 使用的低级 HTTP 客户端 |
| `chardet` / `charset-normalizer` | 字符编码检测（requests 使用其中之一） |

警告在 `requests` 检测到这些依赖的已安装版本**超出其构建支持的版本范围**时触发。修复方法是将所有版本对齐——上面的**选项 1**通常能完全解决问题。

参考资料：

- [requests 更新日志 – 支持的 chardet/charset_normalizer 版本](https://requests.readthedocs.io/en/latest/community/updates/)
- [urllib3/urllib3 GitHub Issue #1571](https://github.com/urllib3/urllib3/issues/1571)
