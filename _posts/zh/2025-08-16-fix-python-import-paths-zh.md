---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复Python模块导入路径
translated: true
type: note
---

简单回答：这里需要 `sys` 是为了在执行 `from scripts.create.delete import delete_md` 之前修改 Python 模块搜索路径（`sys.path`）。

---

### 为什么需要 `sys`

* Python 会在 `sys.path` 存储的目录列表中查找要导入的模块/包。
* 默认情况下，它包含：

  * 当前脚本所在目录
  * 标准库目录
  * 已安装的 site-packages
* 如果你的 `scripts/create/delete.py` 文件不在这些默认位置之一，导入就会失败并提示 `ModuleNotFoundError`。

因此代码这样处理：

```python
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
```

这意味着：

* 获取当前文件的绝对路径（`__file__`）
* 向上返回三级目录
* 将该目录添加到 `sys.path`

之后，Python 就能像处理已安装或在项目根目录中的模块一样解析 `scripts.create.delete`。

---

### 不使用 `sys` 的情况

如果你的项目结构如下：

```
项目/
├── scripts/
│   └── create/
│       └── delete.py
└── tools/
    └── myscript.py   <-- 你正在运行这个文件
```

当你直接运行 `myscript.py` 时，Python 不会自动识别 `项目/` 为根目录。除非你采取以下任一措施，否则导入将失败：

* 使用 `PYTHONPATH=...` 运行（例如 `PYTHONPATH=.. python myscript.py`）
* 将项目打包并安装（`pip install -e .`）
* 在代码中使用 `sys.path.append(...)` 动态添加路径（如示例所示）

---

👉 所以需要 `sys` 纯粹是为了**在运行时操作导入路径**，让你能够导入相对于项目根目录的模块。

需要我为你展示一些**更简洁的替代方案**来避免手动修改 `sys.path` 吗？
