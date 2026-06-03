---
audio: false
generated: true
image: false
lang: zh
layout: post
title: UV同步工作流
translated: true
type: note
---

问题：`uv sync` 的作用是什么？

答案：

`uv sync` 通过读取你的 `pyproject.toml` 或 `uv.lock` 文件，使虚拟环境与项目的依赖保持同步，它做出三个决策：安装缺失的包、升级/降级现有的包以匹配指定的版本。

这是 uv 两阶段依赖工作流中的**同步阶段**：

1. **锁定**（`uv lock`）：解析 `pyproject.toml` → 生成包含固定版本的确定性 `uv.lock`
2. **同步**（`uv sync`）：从 `uv.lock` 安装/更新包到 `.venv`

关键点：同步是将锁文件中所需的包安装到项目开发环境的过程，而锁定和同步都由 uv 自动处理——例如，当你执行 `uv run` 时，项目会在命令调用前完成锁定和同步。

**实际用法：**

```bash
# 显式同步（手动环境设置）
$ uv sync
$ source .venv/bin/activate
$ python script.py

# 隐式同步（推荐 - 更快的反馈循环）
$ uv run python script.py  # 运行前自动同步

# 带选项
$ uv sync --frozen --dev  # 如果锁文件过时则失败；包含开发依赖
$ uv sync --no-dev        # 排除开发依赖
$ uv sync --refresh       # 重新验证所有依赖（清除缓存）
```

**这对你的工作流为何重要：**

由于 uv 极快（尤其在有热缓存时），`uv sync` 基本是瞬间完成的，这意味着你可以在每次运行 Python 命令时同步环境。这消除了手动管理虚拟环境的摩擦。

实际操作：在任何地方用 `uv run` 替代 `python`。你无需手动激活 `.venv`，无需担心过时的包，无需再考虑环境同步——uv 透明地处理这一切。

**CI/生产环境的关键标志：**

- `--frozen`：如果 `uv.lock` 与 `pyproject.toml` 不匹配则失败（可重现构建）
- `--no-sync`：跳过同步（适用于只锁定而不安装的情况）
- `--compile-bytecode`：预编译 `.py` 为 `.pyc`（节省冷启动时的导入时间）

参考：

- [uv Locking and Syncing](https://docs.astral.sh/uv/concepts/projects/sync/)
- [uv Working on Projects](https://docs.astral.sh/uv/guides/projects/)
