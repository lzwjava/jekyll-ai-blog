---
audio: false
generated: true
image: false
lang: zh
layout: post
title: GPU冒烟测试总结
translated: true
type: note
---

冒烟测试运行完成。✅ 以下是总结：

## 结果

| 测试 | 命令 | 结果 |
|------|---------|--------|
| 导入检查 | `python3.12 -c "import sglang, torch"` | ✅ sglang dev63, torch 2.11+cu130, CUDA 可用 |
| 单元测试 | `python3.12 test/registered/unit/configs/test_embedding_model_spec.py -f` | ✅ 6 项测试通过 |
| 注册 CLI 测试 | `python3.12 test/registered/unit/cli/test_serve_backends.py -f` | ✅ 12 项测试通过 |
| **GPU 推理冒烟测试** (Qwen2.5-1.5B-Instruct) | 引擎启动 + `engine.generate()` | ✅ "The capital of France is" → **" Paris, which is at latitude 48.85..."** 耗时约 4 秒 |

## 过程中发现并修复的问题

1. **Python 环境**：默认 `python3` 为 3.14 (linuxbrew)；改用 `/usr/bin/python3.12` (3.12.3，sglang 以开发模式安装在 `/mnt/data/sglang/python`)。
2. **内核版本不匹配**：仓库要求 `sglang-kernel >= 0.4.6.post1`，但 0.4.6.post1 在 PyPI 上唯一的 wheel 仅提供 **SM100 专属二进制**（无法在你的 RTX 4070/SM89 上加载，且存在 torch ABI 不匹配）。回退至 **0.4.5**（包含 sm90/sm89 兼容二进制），并使用以下命令运行：
   ```bash
   env SGLANG_SKIP_SGL_KERNEL_VERSION_CHECK=1
   ```
3. **默认测试模型** (`meta-llama/Llama-3.2-1B-Instruct`) 需要授权且未缓存；改用本地缓存的 `Qwen/Qwen2.5-1.5B-Instruct`。
4. **DeepSeek-V2-Lite 在 12GB 显卡上 OOM**；本地冒烟测试限制使用 ≤1.5B 的模型。

## 可行的冒烟测试命令

```bash
cd /mnt/data/sglang && env SGLANG_SKIP_SGL_KERNEL_VERSION_CHECK=1 HF_HUB_OFFLINE=1 \
  /usr/bin/python3.12 /tmp/smoke_sglang.py
```

注意：此仓库检出版本领先于已发布的 `sglang-kernel` wheel 对 SM89 的支持，因此在匹配的内核 wheel 发布之前，完整的 GPU CI 套件（`run_suite.py --hw cuda ...`）无法在本地运行。CPU 套件（`base-a-test-cpu`）和单元测试运行正常。