---
audio: false
generated: true
image: false
lang: en
layout: post
title: SGLang IDE Support Overview
translated: false
type: note
---

Here's what I found in the repo (`/mnt/data/sglang`):

## There is no official "recommended IDE" doc

No doc (`README.md`, `docs_new/`, `CONTRIBUTING.md`, `developer_guide/`) names a specific IDE. The contribution guide only covers source install, pre-commit, pytest, and the dev docker image. But the repo ships strong signals for both **VS Code** and **PyCharm**:

## 1. VS Code — the officially supported setup

The repo includes an official dev container: `.devcontainer/devcontainer.json` + `Dockerfile`. Its `customizations` section is VSCode-specific and auto-recommends these extensions:

| Extension | Why |
| --- | --- |
| `ms-python.python` | Python core |
| `charliermarsh.ruff` | Matches the repo's ruff pre-commit hook (`.pre-commit-config.yaml`) |
| `rust-lang.rust-analyzer` | SGLang now has Rust code (`rust/sglang-grpc`, `sgl-model-gateway/`) |
| `tamasfe.even-better-toml` | TOML configs |

The container is built from `lmsysorg/sglang:dev`, passes through GPUs (`--gpus all`), bind-mounts your repo for live sync into the installed sglang pip package, and sets up a non-root `devuser` with zsh + uv. This is the closest thing to a "recommended" dev environment — a one-click VS Code remote-container dev loop.

## 2. PyCharm / JetBrains — used by maintainers

A `.idea/` directory is committed to the repo with full project files:

- Modules: `sglang.iml`, `sglang-server.iml`, `sglang-kernel.iml`, `sglang-mm.iml`, `sglang-router.iml`, `sglang-grpc.iml`, `flash-attn-4.iml`, `sgl-model-gateway-e2e-tests.iml`, `amd-sglang.iml`
- Config: Python 3.12 SDK (`/usr/bin/python3.12`), `py.test` as the test runner, ReST support

So at least some core developers work in PyCharm/IntelliJ. Open the root and it just works.

## 3. Zed — zero mention

`rg` for `zed` found nothing anywhere in the repo. It would work fine (it's a general Python/Rust editor), but there's no official config, extension list, or setup for it.

## Bottom line

- **VS Code** if you want the officially-supported, zero-config GPU dev container (recommend — the `.devcontainer` was clearly built for it).
- **PyCharm (or IntelliJ IDEA)** if you prefer JetBrains — the checked-in `.idea/` files mean it's actively used by the project.
- **Zed** — nothing official; you'd configure it yourself (ruff, rust-analyzer, pytest, and the dev docker image for GPU work).

Either way, the real contract is the tooling, which is IDE-agnostic: pre-commit (ruff + isort for Python, clang-format for CUDA/C++ kernels), pytest for tests, and `lmsysorg/sglang:dev` docker image for GPU development.
