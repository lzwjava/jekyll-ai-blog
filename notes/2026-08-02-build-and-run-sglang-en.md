---
audio: false
generated: true
image: false
lang: en
layout: post
title: Build and Run SGLang
translated: false
type: note
---

This is **SGLang**, a high-performance LLM serving framework (Python + PyO3 Rust extensions). Here's how to build it and start working with it.

## Project layout

- `python/` — main Python package (`sglang`), built with `setuptools` + `setuptools-rust`
- `rust/` — Cargo workspace with 3 PyO3 extension crates (`sglang-grpc`, `sglang-mm`, `sglang-server`); auto-discovered and compiled during `pip install`
- `python/setup.py` — build hooks; `SGLANG_BUILD_RUST_EXTS` env var controls which Rust ext gets built (`all`/`none`/substring list, e.g. `"grpc"`)
- `docs_new/` — documentation site; `test/` — unit + e2e tests

## How to compile (build from source)

The official way (from `docs_new/docs/get-started/install.mdx`):

```bash
cd /mnt/data/sglang
pip install --upgrade pip
pip install -e "python"        # editable install; builds the Rust extensions too
```

It needs: Python ≥ 3.10, CUDA, a Rust toolchain (pinned to **1.90** via `rust/rust-toolchain.toml`), and `ninja`. The first build compiles 3 Rust crates + JIT-kernels, so expect it to take a while.

### Notes specific to this machine

- **Python version**: `python3` here is 3.14 (Linuxbrew). This repo pins `torch==2.11.0` and heavy CUDA deps (`flashinfer_python[cu13]`, `sglang-kernel`, `sgl-deep-gemm`). Safest bet is a venv on **Python 3.12** (available at `/usr/bin/python3.12`) — 3.14 is risky for torch/CUDA wheels.
- **Disk**: `/` has only 11 GB free (99% full) — the venv, pip cache, and torch (~10 GB) won't fit there. Put everything under `/mnt/data`:

  ```bash
  export PIP_CACHE_DIR=/mnt/data/pip-cache
  /usr/bin/python3.12 -m venv /mnt/data/sglang-venv
  source /mnt/data/sglang-venv/bin/activate
  pip install --upgrade pip
  pip install -e "python"
  ```

- **CUDA**: driver is CUDA 13.0 and `cuda-13.2` toolchain is installed, matching this main-branch checkout (CUDA 13 default). Set `export CUDA_HOME=/usr/local/cuda-13.2` if the build complains it's unset.
- **GPU**: RTX 4070 (12 GB) — fine for small/medium models (Qwen2-0.5B/1.5B, Llama-3.1-8B with quantization).

## How to start working

**1. Launch a server** (the entry point is `python/sglang/launch_server.py`):

```bash
python3 -m sglang.launch_server --model-path Qwen/Qwen2-0.5B-Instruct --host 0.0.0.0 --port 30000
```

**2. Send a request** (OpenAI-compatible API):

```bash
curl http://localhost:30000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "Qwen/Qwen2-0.5B-Instruct", "messages": [{"role": "user", "content": "Hello"}]}'
```

**3. Run tests**:

```bash
pytest test/registered/unit/ -v                    # all unit tests
pytest test/registered/unit/mem_cache/ -v          # one module
```

Unit tests mirror `python/sglang/srt/` under `test/registered/unit/` — add tests there when you change `srt/` code.

**4. Lint before committing** (repo uses pre-commit: ruff, isort, trailing-whitespace, etc.):

```bash
pip install pre-commit && pre-commit install
pre-commit run --all-files
```

**5. Dev workflow tips** (from the contribution guide):

- Never commit to `main`; work on feature branches
- Code lives in `python/sglang/srt/` (runtime: scheduler, models, mem_cache, sampling…)
- [Mini-SGLang](https://github.com/sgl-project/mini-sglang) is a good starter for understanding the code structure
- Easy entry points: issues labeled `good first issue` / `help wanted`

**Note on development mode**: with `pip install -e "python"`, Python changes are picked up instantly, but the Rust extensions (`rust/`) are compiled once at install time — after editing `rust/`, re-run `pip install -e "python"` to rebuild them.

Want me to go ahead and set up the Python 3.12 venv on `/mnt/data` and run the build?
