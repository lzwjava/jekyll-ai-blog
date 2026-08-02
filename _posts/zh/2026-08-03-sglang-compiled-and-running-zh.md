---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SGLang 编译并运行
translated: true
type: note
---

一切已设置并验证可正常工作。以下是完整摘要：

## 已完成：SGLang 编译并运行

**Build**（安装到系统 Python 3.12 的 user site，无 venv）：

```
/usr/bin/python3.12 -m pip install -e "python" --user --break-system-packages
```

- PEP 668 需要 `--break-system-packages`；packages 安装至 `~/.local/lib/python3.12/site-packages`
- Editable install：`/mnt/data/sglang/python/` 中的 Python 更改立即生效
- 所有 3 个 Rust extensions（`sglang.srt.grpc._core`、`sglang.srt.multimodal._core`、`sglang.srt.server._core`）均已编译到 source tree 中
- 修复了预先存在的 torch/torchvision/torchaudio CUDA 不匹配问题 — 现均为 `2.11.0+cu130`

**当前运行：** Qwen2.5-0.5B-Instruct server 位于 `http://localhost:30010`（PID 2170340）。已验证：chat completion → "Paris" ✓

## 发现的两个机器特定问题

1. **HF Xet 下载停滞** — model downloads 在约 84 MB 处冻结，直到我禁用 transfer protocol。始终设置：

   ```bash
   export HF_HUB_DISABLE_XET=1
   ```

2. **端口 30000/30001 被此机器上的其他应用占用**（`cef_server` 和 PyCharm）。请使用例如 `--port 30010`。

## 使用项目

```bash
# 启动 server（推荐 entrypoint）
export HF_HUB_DISABLE_XET=1
python3.12 -m sglang.launch_server --model-path Qwen/Qwen2.5-0.5B-Instruct --port 30010

# 发送请求（OpenAI compatible）
curl http://localhost:30010/v1/chat/completions -H "Content-Type: application/json" \
  -d '{"model": "Qwen/Qwen2.5-0.5B-Instruct", "messages": [{"role": "user", "content": "Hi!"}]}'

# Unit tests（镜像 python/sglang/srt/ 到 test/registered/unit/）
pytest test/registered/unit/ -v

# 提交前进行 lint
pre-commit install && pre-commit run --all-files
```

**开发工作流说明：**

- Python 编辑 → 只需重启 server（editable install）
- Rust 编辑（`rust/`）→ 重新运行 `pip install -e "python"` 以重新构建
- 使用 `sglang serve` 作为 CLI（这是新的推荐 entrypoint；`launch_server` 仍可用，但会显示 deprecation warning）
- 在 feature branch 上工作，永远不要在 `main` 上；检查 `.github/CI_PERMISSIONS.json` 获取 CI-trigger commands（`/rerun-failed-ci` 等）

Server 保持运行 — 随时用 `pkill -f sglang.launch_server` 停止它。需要我停止它，还是设置其他内容（例如 `bench_serving` run 或不同 model）？
