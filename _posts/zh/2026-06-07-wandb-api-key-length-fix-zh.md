---
audio: false
generated: true
image: false
lang: zh
layout: post
title: WandB API密钥长度修复
translated: true
type: note
---

**问题：** 在 nanochat 训练脚本中，`tracker=wandb` 参数如何工作？为什么 WandB 抱怨 API key 格式不是 48 字符？

**答案：**

`tracker=wandb` 参数告诉训练脚本将指标、梯度和样本记录到 Weights & Biases。WandB 关于 key 长度的抱怨表明你正在使用**旧的 API key 格式**或**过时的 WandB 版本**。

## 工作原理

该脚本很可能在 `scripts/base_train.py` 中早期初始化 WandB：

```python
if config.tracker == "wandb":
    import wandb
    wandb.init(project="nanochat", config=config)
```

WandB 按以下优先级读取你的 API key：

1. `WANDB_API_KEY` 环境变量
2. `~/.netrc` 文件（来自 `wandb login`）
3. `.wandb` 本地目录

## 48 字符问题

**WandB 在 2024 年中左右更改了 API key 格式：**

- **旧格式：** 40 字符十六进制字符串
- **新格式：** 48 字符字母数字字符串（看起来像 `wab_<...>`）

如果 WandB 抱怨 48 字符，说明它期望**新格式**，意味着你的旧 key 已失效。

## 修复方法（三步）

**步骤 1：重新生成 key**

```bash
# 退出旧会话
wandb logout

# 重新登录（打开浏览器，生成新 key）
wandb login
```

粘贴来自 <https://wandb.ai/authorize> 的新 key（应为 48 字符，以 `wab_` 开头）。

**步骤 2：确认已保存**

```bash
cat ~/.netrc | grep wandb
# 应显示类似：password wab_xxxxxxxxxxxxxxxxxxxxx
```

**步骤 3：或通过环境变量设置**

```bash
export WANDB_API_KEY="wab_xxxxxxxxxxxxxxxxxxxxx"

# 然后运行训练
cd /mnt/data/nanochat && PYTORCH_ALLOC_CONF=expandable_segments:True .venv/bin/python -m scripts.base_train \
  --run=rtx4070-d12-200k \
  --tracker=wandb \
  ...
```

## 替代方案：如果只想训练，跳过 WandB

如果 WandB 拖慢速度或增加麻烦，可以使用 `--tracker=none` 或将其注释掉：

```bash
# ... --tracker=none ...
```

然后通过 tensorboard、原始日志或解析训练输出来本地监控 loss。

**专业提示：** 对于像 200k 次迭代这样的长训练，WandB 是值得的（保存运行检查点，允许跨机器重启跟踪）。但请确保你的 key 是最新的——重新生成一次即可。
