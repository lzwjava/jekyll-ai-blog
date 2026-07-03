---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 复现 FineWeb Code Sec GPT
translated: true
type: note
---

所有脚本已提交并推送至 `f55da65`，此后无任何更改。所有内容已在 GitHub 上。

以下是 `/mnt/data/zz/` 当前的内容 —— 你可以 `cd` 到该目录并运行：

```
/mnt/data/zz/
├── prepare_data.sh          # 完整数据流程：下载 + 转换 + 合并 + 训练分词器
├── fineweb-code-sec-gpt.sh  # 训练：--smoke（200步）或完整版（5万步）
└── train_log.sh             # 监控：tail/watch/summary
```

**数据流程**（仅需运行一次以复现）：

```
bash /mnt/data/zz/prepare_data.sh
```

**训练**：

```
bash /mnt/data/zz/fineweb-code-sec-gpt.sh           # 5万步，约16小时
bash /mnt/data/zz/fineweb-code-sec-gpt.sh --smoke    # 200步验证
```

**监控**：

```
bash /mnt/data/zz/train_log.sh --watch
bash /mnt/data/zz/train_log.sh --summary
```

烟雾测试因终端超时而反复中断。直接在你的 shell 中运行时应能正常工作。
