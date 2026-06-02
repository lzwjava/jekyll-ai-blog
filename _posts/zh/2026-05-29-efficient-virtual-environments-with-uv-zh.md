---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用uv的高效虚拟环境
translated: true
type: note
---

问题：如果我们使用 `uv`，它是否会因为每个项目都创建虚拟环境而消耗大量磁盘空间？

答案：

使用 [uv](https://github.com/astral-sh/uv?utm_source=chatgpt.com) 通常**不会**像人们最初预期的那样消耗大量磁盘空间，即使它为每个项目创建了独立的虚拟环境（`.venv`）。

原因如下。

---

## 为什么 `uv` 比传统的 `venv + pip` 更节省磁盘空间

`uv` 积极使用：

* **全局包缓存**
* 尽可能使用硬链接/符号链接
* 共享的 wheel 存储
* 非常快速的依赖解析

因此，尽管每个项目都有自己的 `.venv`，实际包文件通常是从全局缓存中复用，而不是重复复制。

这类似于：

* `pnpm` 在 Node.js 中的工作方式
* `Nix` 存储的工作方式
* Docker 层缓存的工作方式

---

## 实际占用空间的是什么

典型的 Python 虚拟环境内容：

| 组件               | 空间占用       |
| ------------------ | -------------- |
| Python 解释器      | 小到中等       |
| 已安装的包         | 主要占用       |
| 缓存/wheels        | 由 `uv` 共享   |
| 项目源代码         | 通常很小       |

使用经典的 `pip + venv` 时，包通常被重复复制。

使用 `uv` 时，许多文件通过缓存复用。

---

## 实际案例

假设你有：

* 20 个项目
* 每个项目使用：

  * `numpy`
  * `pandas`
  * `torch`
  * `fastapi`

传统的隔离 venv 可能会重复复制数 GB 的数据。

`uv` 可以复用大部分包工件。

因此：

* 项目元数据保持独立
* 依赖保持隔离
* 磁盘重复显著减少

---

## 但大型机器学习包仍然占用空间

有些包本身非常大：

| 包                 | 近似大小       |
| ------------------ | -------------- |
| PyTorch CUDA       | 2–6 GB         |
| TensorFlow         | 1–3 GB         |
| CUDA 工具包        | 5–20 GB        |
| Transformers 模型  | 巨大           |

即使有缓存，这些包仍然在全局范围内占用大量存储空间。

所以在 AI/ML 工作流程中，最大的问题通常是：

* 模型检查点
* 数据集
* CUDA 运行时

——而不是虚拟环境本身。

---

## 与其他工具对比

| 工具             | 磁盘效率                |
| ---------------- | ----------------------- |
| `pip + venv`     | 低                      |
| `poetry`         | 中                      |
| `conda`          | 高（重）                |
| `uv`             | 非常好                  |
| `pixi` / `nix`   | 优秀但更复杂            |

`conda` 环境通常比 `uv` 重得多。

---

## 一个重要细节

如果项目需要：

* 不同的 Python 版本
* 不同的 CUDA 构建
* 不兼容的二进制 wheel

那么有些重复是不可避免的。

例如：

* Python 3.10 与 3.12
* CPU 版与 CUDA 版 PyTorch
* 不同 NumPy ABI 版本

这些不能总是安全地共享二进制文件。

---

## 典型磁盘使用模式

你可能会看到：

```bash
project-a/.venv
project-b/.venv
project-c/.venv
```

但实际的包数据大部分存放在：

```bash
~/.cache/uv/
```

因此，删除一个项目通常只移除轻量级的元数据和链接。

---

## 实用建议

对于现代 Python 开发，尤其是 AI/后端/全栈工作：

* `uv` 目前通常是最佳选择之一
* 比 `pip` 快得多
* 通常更节省空间
* 更干净的依赖隔离
* 非常适合多项目工作流

许多工程师正在转向：

* `uv`
* `rye`
* `pixi`
* `mise`

而不是传统的 `pip + virtualenv`。

参考资料：

* [https://github.com/astral-sh/uv](https://github.com/astral-sh/uv)
* [https://docs.astral.sh/uv/](https://docs.astral.sh/uv/)
* [https://github.com/astral-sh/uv/blob/main/docs/concepts/cache.md](https://github.com/astral-sh/uv/blob/main/docs/concepts/cache.md)
