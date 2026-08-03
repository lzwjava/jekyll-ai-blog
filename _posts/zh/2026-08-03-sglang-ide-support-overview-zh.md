---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SGLang IDE 支持概述
translated: true
type: note
---

以下是我在仓库（`/mnt/data/sglang`）中的发现：

## 没有官方的“推荐 IDE”文档

没有任何文档（`README.md`、`docs_new/`、`CONTRIBUTING.md`、`developer_guide/`）指定了具体的 IDE。贡献指南只涵盖了源码安装、pre-commit、pytest 和开发 docker 镜像。但仓库为 **VS Code** 和 **PyCharm** 都提供了明确的信号：

## 1. VS Code — 官方支持的配置

仓库包含一个官方的开发容器：`.devcontainer/devcontainer.json` + `Dockerfile`。其 `customizations` 部分是针对 VSCode 的，并自动推荐以下扩展：

| 扩展 | 原因 |
| --- | --- |
| `ms-python.python` | Python 核心支持 |
| `charliermarsh.ruff` | 与仓库的 ruff pre-commit 钩子（`.pre-commit-config.yaml`）匹配 |
| `rust-lang.rust-analyzer` | SGLang 现在包含 Rust 代码（`rust/sglang-grpc`、`sgl-model-gateway/`） |
| `tamasfe.even-better-toml` | TOML 配置文件 |

该容器基于 `lmsysorg/sglang:dev` 构建，透传 GPU（`--gpus all`），将你的仓库绑定挂载以实时同步到已安装的 sglang pip 包中，并设置了非 root 用户 `devuser`，使用 zsh + uv。这是最接近“推荐”开发环境的东西——一个一键式的 VS Code 远程容器开发循环。

## 2. PyCharm / JetBrains — 维护者使用的环境

仓库中提交了一个 `.idea/` 目录，包含完整的项目文件：

- 模块：`sglang.iml`、`sglang-server.iml`、`sglang-kernel.iml`、`sglang-mm.iml`、`sglang-router.iml`、`sglang-grpc.iml`、`flash-attn-4.iml`、`sgl-model-gateway-e2e-tests.iml`、`amd-sglang.iml`
- 配置：Python 3.12 SDK（`/usr/bin/python3.12`）、`py.test` 作为测试运行器，支持 ReST

因此，至少部分核心开发者在 PyCharm/IntelliJ 中工作。打开根目录即可直接使用。

## 3. Zed — 完全没有提到

对 `zed` 的 `rg` 搜索在仓库中没有任何发现。它应该可以正常使用（这是一个通用的 Python/Rust 编辑器），但没有官方的配置、扩展列表或相关设置。

## 结论

- **VS Code**——如果你想要官方支持、零配置的 GPU 开发容器（推荐——`.devcontainer` 显然是为它构建的）。
- **PyCharm（或 IntelliJ IDEA）**——如果你更喜欢 JetBrains——仓库中已提交的 `.idea/` 文件表明项目正在积极使用它。
- **Zed**——没有任何官方支持；你需要自行配置（ruff、rust-analyzer、pytest，以及用于 GPU 工作的开发 docker 镜像）。

无论哪种方式，真正的约定是工具链，它与 IDE 无关：pre-commit（针对 Python 的 ruff + isort，针对 CUDA/C++ 内核的 clang-format）、用于测试的 pytest，以及用于 GPU 开发的 `lmsysorg/sglang:dev` docker 镜像。
