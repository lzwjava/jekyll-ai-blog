---
audio: false
generated: true
image: false
lang: zh
layout: post
title: HuggingFace 中国下载指南
translated: true
type: note
---

**两个环境变量完成所有工作：**

| 变量                               | 作用                                                                                     |
| ---------------------------------- | ---------------------------------------------------------------------------------------- |
| `HF_ENDPOINT=https://hf-mirror.com` | 将所有 HF Hub 流量路由至国内镜像。无需代理，不影响你的 DMIT VPS。                        |
| `HF_HUB_ENABLE_HF_TRANSFER=1`      | 使用 Rust `hf_transfer` 客户端实现并行多块下载（快 5–10 倍）。需先执行 `pip install hf_transfer`。 |

## 一次性命令

```bash
HF_ENDPOINT=https://hf-mirror.com HF_HUB_ENABLE_HF_TRANSFER=1 \
  python3.11 sample.py --init_from=gpt2-medium --start="Hello" --num_samples=1
```

## 永久生效（推荐）

添加到 `~/.bashrc` 中，以免忘记：

```bash
export HF_ENDPOINT=https://hf-mirror.com
export HF_HUB_ENABLE_HF_TRANSFER=1
```

然后执行 `source ~/.bashrc`。所有使用 `transformers` / `datasets` / `huggingface_hub` 的 Python 脚本都会自动加载这些设置。

## 预下载（避免训练中途下载）

```bash
huggingface-cli download gpt2-medium                              # 模型
huggingface-cli download HuggingFaceFW/fineweb --repo-type=dataset --include="sample/10BT/*"  # 数据集
```

文件会保存到 `~/.cache/huggingface/hub/` 中，后续每次调用 `from_pretrained()` 都会复用这些文件。

## 适用范围

- `GPT.from_pretrained("gpt2-medium")` ← nanoGPT 的 `sample.py` 所用的调用方式
- `AutoModel.from_pretrained(...)`, `AutoTokenizer.from_pretrained(...)`
- `datasets.load_dataset("HuggingFaceFW/fineweb", ...)` ← 你的 fineweb 运行
- `huggingface-cli download ...`

## 注意事项

- **`hf_transfer` 没有进度重试机制** — 如果下载中途失败，会直接报错退出，而非断点续传。若反复失败，请取消设置 `HF_HUB_ENABLE_HF_TRANSFER`，然后使用标准客户端重试。
- **镜像延迟** — `hf-mirror.com` 会以较短延迟镜像公共 Hub。全新发布的模型（当天发布）可能在几小时内返回 404。
- **私有/限权模型** — 镜像仅提供公共文件。对于限权仓库（如 Llama 等），仍需 `HF_TOKEN` 且可能需使用真实端点。
- **不要与代理同时使用** — 如果设置了 `HTTPS_PROXY`，请在对 HF 的调用中取消它，否则又会消耗你的 DMIT 带宽。

## 验证是否生效

```bash
HF_ENDPOINT=https://hf-mirror.com huggingface-cli download gpt2 --quiet
echo $?   # 0 表示成功
```

或者观察进度条中的 URL — 应显示 `hf-mirror.com`，而非 `huggingface.co`。
