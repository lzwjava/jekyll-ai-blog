---
audio: false
generated: true
image: false
lang: zh
layout: post
title: huggingface_hub并不是遗留系统
translated: true
type: note
---

问题：`huggingface_hub` 现在过时了吗？`hf` 是最新的 CLI 吗？（我运行 `hf --version` 得到 1.12.0）

答案：

没有过时——你把两件事混淆了。`huggingface_hub` 是 **Python 包**，并且它非常活跃。`hf` 只是它的 **CLI 入口点的新名称**，该入口点*包含在*同一个包中。

实际变化如下：

- 旧命令是 `huggingface-cli`。它被重命名为 `hf`（更简洁的动词-名词语法），旧名称已被弃用。
- `hf --version 1.12.0` 显示的是 `huggingface_hub` 包本身的版本——它们共享版本号，因为 CLI 是库的一部分。

因此：

```bash
pip show huggingface_hub   # 这就是 hf --version 报告的内容
hf --help                  # 新 CLI（huggingface-cli 仍可用但会发出警告）
```

新语法是 `hf <资源> <操作>`：

```bash
hf auth login              # 原为：huggingface-cli login
hf download <repo>         # 原为：huggingface-cli download <repo>
hf upload <repo> <path>    # 原为：huggingface-cli upload
hf auth whoami
hf repo create <name>
```

在 Python 中没有任何变化——你仍然导入相同的内容：

```python
from huggingface_hub import HfApi, snapshot_download, hf_hub_download
```

值得确认确切的重命名时间线以及哪个版本改变了默认行为，因为这类 CLI 更新很快，我不应该凭记忆猜测：根据来源确认——你的 `1.12.0` 已经说明了一切：

- `hf` CLI 是从 `huggingface-cli` 重命名而来的，作为一项生活质量改进，在 v0.34 中引入，遵循 `hf <资源> <操作>` 的语法。
- 在 huggingface_hub v1.0 中，已弃用的 `huggingface-cli` 被完全移除，重新设计的 `hf` CLI（现在基于 Typer）取代了它。如果你正在编写脚本与之交互，v1.0 中其他值得注意的破坏性变更包括：迁移到 httpx 作为 HTTP 后端，以及 hf_xet 成为默认的文件传输包，取代了已移除的 hf_transfer。
- 对于你的训练栈，一个兼容性问题需要注意：transformers v4 明确要求 huggingface_hub v0.x，而 transformers v5 要求 v1.x。由于你使用的是 `1.12.0`，你需要 transformers v5——如果某个依赖固定了旧版 transformers，你会遇到解析器冲突。

总结：`huggingface_hub` = 库（当前版本，你用的是 1.12.0）。`hf` = 它的 CLI（当前版本）。`huggingface-cli` = 已淘汰的名称。你完全是最新版本。

在 sec-edgar GPT 工作中你会实际用到的命令快速参考：

```bash
hf auth login
hf download <org>/<model>           # 拉取权重/分词器
hf upload <org>/<repo> ./out        # 单次提交
hf upload-large-folder <repo> ./ckpt  # 可续传，用于大型检查点
hf cache ls --filter "size>1GB"     # 新的 v1.0 Docker 风格缓存管理
hf jobs run --flavor a10g-small ...  # 在 HF 硬件上运行脚本
```

在 MI300X 机器上值得设置一个环境变量来在非交互式运行中禁用启动时的自动更新检查：`export HF_HUB_DISABLE_UPDATE_CHECK=1`。

参考：

- [Say hello to `hf`: a faster, friendlier Hugging Face CLI](https://huggingface.co/blog/hf-cli)
- [huggingface_hub v1.0 release blog](https://huggingface.co/blog/huggingface-hub-v1)
- [Migrating to huggingface_hub v1.0](https://huggingface.co/docs/huggingface_hub/en/concepts/migration)
