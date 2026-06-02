---
audio: false
generated: true
image: false
lang: zh
layout: post
model: x-ai/grok-4.1-fast
title: 在 Windows 上将 ibm_db 与捆绑的 clidriver 结合使用
translated: true
type: note
---

问题：我们可以在 Windows 上使用 IBM 提供的 `clidriver`（`ibm_db` 包附带的私有 DB2 客户端）来避免“DLL 无法加载”错误吗？

答案：

是的 – 这实际上是 Windows 上目前**最简单和最推荐的方法**。

IBM 维护一个名为 **ibm_db_clidriver** 的特殊包（也可以通过 `ibm_db[clidriver]` 简单安装），它包含一个完整、私有的 64 位 DB2 运行时客户端副本（包括 `db2cli64.dll` 和所有依赖项）。
安装此包后，`import ibm_db` 会立即工作，无需更改 PATH，无需 `os.add_dll_directory()`，也无需单独安装 DB2 客户端。

### 如何使用（2025 年，当前方法）

```bash
# 选项 1 – 推荐（一行）
pip install "ibm_db[clidriver]"

# 选项 2 – 明确（结果相同）
pip install ibm_db
pip install ibm_db_clidriver
```

就这样。现在这在任何地方都适用：

```python
import ibm_db          # ← 不再有 DLL 错误
conn = ibm_db.connect("DATABASE=mydb;HOSTNAME=server;PORT=50000;UID=user;PWD=pass;", "", "")
```

### 幕后发生了什么

- `clidriver` 会被解压到 `<your-python-site-packages>/clidriver`
- 示例路径：
  `C:\Python312\Lib\site-packages\clidriver\bin\amd64.VC12`
- `ibm_db` 在导入时会自动将这个私有的 `clidriver\bin` 目录添加到 DLL 搜索路径中，因此即使系统 PATH 中没有任何内容，Windows 也能找到 `db2cli64.dll`。

### 优点对比单独安装 DB2 客户端

| 方法                            | 需要更改系统 PATH 吗？ | 需要 os.add_dll_directory() 吗？ | 在虚拟环境中工作吗？ | 只需 pip install 即可工作吗？ | 大小       |
| ------------------------------- | ---------------------- | -------------------------------- | -------------------- | ----------------------------- | ---------- |
| 独立的 IBM Data Server Client   | 是                     | 有时                             | 仅当 PATH 全局设置时 | 否                            | ~300–800 MB |
| ibm_db[clidriver]               | 否                     | 否                               | 是                   | 是                            | ~120 MB    |

### 何时您可能仍然倾向于使用完整的独立客户端

- 您已经有（Python 之外的）应用程序需要 DB2 客户端。
- 您需要非常新的修复程序或功能，这些功能尚未包含在捆绑的 clidriver 中。
- 公司政策禁止在 Python 包中捆绑运行时库。

否则，只需使用捆绑的 clidriver – 这是目前 Windows 上大多数人的做法。

参考资料：

- [python-ibmdb – 使用 ibm_db_clidriver 包](https://github.com/ibmdb/python-ibmdb#using-ibm_db_clidriver-package)
- [ibm_db PyPI 页面 – clidriver 额外包](https://pypi.org/project/ibm-db/)
