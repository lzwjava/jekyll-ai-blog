---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 构建并运行 SGLang
translated: true
type: note
---

这是 **SGLang**，一个高性能的 LLM 服务框架（Python + PyO3 Rust 扩展）。下面说明如何构建并开始使用它。

## 项目结构

- `python/` — 主要 Python 包（`sglang`），使用 `setuptools` + `setuptools-rust` 构建
- `rust/` — Cargo 工作区，包含 3 个 PyO3 扩展 crate（`sglang-grpc`、`sglang-mm`、`sglang-server`）；在 `pip install` 时自动发现并编译
- `python/setup.py` — 构建钩子；`SGLANG_BUILD_RUST_EXTS` 环境变量控制构建哪个 Rust 扩展（`all`/`none`/子串列表，例如 `"grpc"`）
- `docs_new/` — 文档站点；`test/` — 单元测试和端到端测试

## 如何编译（从源码构建）

官方方式（来自 `docs_new/docs/get-started/install.mdx`）：

```bash
cd /mnt/data/sglang
pip install --upgrade pip
pip install -e "python"        # 可编辑安装；同时构建 Rust 扩展
```

需要：Python ≥ 3.10、CUDA、Rust 工具链（通过 `rust/rust-toolchain.toml` 固定为 **1.90**）以及 `ninja`。首次构建会编译 3 个 Rust crate 和 JIT 内核，因此需要一段时间。

### 针对此机器的注意事项

- **Python 版本**：此处的 `python3` 是 3.14（Linuxbrew）。本仓库固定使用 `torch==2.11.0` 和较重的 CUDA 依赖（`flashinfer_python[cu13]`、`sglang-kernel`、`sgl-deep-gemm`）。最稳妥的方式是在 **Python 3.12**（路径 `/usr/bin/python3.12`）上创建虚拟环境——3.14 对 torch/CUDA 轮子来说风险较大。
- **磁盘**：`/` 仅有 11 GB 可用空间（99% 已满）——虚拟环境、pip 缓存和 torch（约 10 GB）无法放入。请将所有内容放在 `/mnt/data` 下：
  ```bash
  export PIP_CACHE_DIR=/mnt/data/pip-cache
  /usr/bin/python3.12 -m venv /mnt/data/sglang-venv
  source /mnt/data/sglang-venv/bin/activate
  pip install --upgrade pip
  pip install -e "python"
  ```
- **CUDA**：驱动为 CUDA 13.0，且已安装 `cuda-13.2` 工具链，与当前主分支检出（默认 CUDA 13）匹配。如果构建时提示未设置，请执行 `export CUDA_HOME=/usr/local/cuda-13.2`。
- **GPU**：RTX 4070（12 GB）——适合小型/中型模型（Qwen2-0.5B/1.5B、Llama-3.1-8B 量化版本）。

## 如何开始工作

**1. 启动服务端**（入口点为 `python/sglang/launch_server.py`）：
```bash
python3 -m sglang.launch_server --model-path Qwen/Qwen2-0.5B-Instruct --host 0.0.0.0 --port 30000
```

**2. 发送请求**（兼容 OpenAI API）：
```bash
curl http://localhost:30000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "Qwen/Qwen2-0.5B-Instruct", "messages": [{"role": "user", "content": "Hello"}]}'
```

**3. 运行测试**：
```bash
pytest test/registered/unit/ -v                    # 所有单元测试
pytest test/registered/unit/mem_cache/ -v          # 单个模块
```
单元测试在 `test/registered/unit/` 下与 `python/sglang/srt/` 保持镜像——修改 `srt/` 代码时请在此添加测试。

**4. 提交前进行 lint**（仓库使用 pre-commit：ruff、isort、trailing-whitespace 等）：
```bash
pip install pre-commit && pre-commit install
pre-commit run --all-files
```

**5. 开发工作流程建议**（来自贡献指南）：
- 绝不直接提交到 `main`；在功能分支上工作
- 代码位于 `python/sglang/srt/`（运行时：调度器、模型、内存缓存、采样等）
- [Mini-SGLang](https://github.com/sgl-project/mini-sglang) 是理解代码结构的良好起点
- 简单入口：标有 `good first issue` / `help wanted` 的 issue

**关于开发模式的说明**：使用 `pip install -e "python"` 后，Python 改动会立即生效，但 Rust 扩展（`rust/`）仅在安装时编译一次——编辑 `rust/` 后，请重新运行 `pip install -e "python"` 以重新构建。

需要我继续在 `/mnt/data` 上设置 Python 3.12 虚拟环境并执行构建吗？