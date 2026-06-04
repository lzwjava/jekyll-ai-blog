---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 模型迁移与令牌查询
translated: true
type: note
---

完成。以下为发生的情况：

```
Remote switched:  github.com/lzwjava/zz  ->  huggingface.co/lzwjava/zz
Fast-forward merge: 108bc6b..9db74d9 (9 files, +2593 lines)

New content pulled:
  - 760M model inference samples (code, facts, story, ai_history)
  - 760M training logs from MI300X run
  - inference quality audit
  - FineWeb download script for AMD/US environment
```

对于推送，你需要 HF 认证。准备好后运行：

```
huggingface-cli login
```

或者如果你想使用 token：

```
git config --global credential.helper store
echo "https://lzwjava:YOUR_HF_TOKEN@huggingface.co" >> ~/.git-credentials
```

现在——想要我深入查看 zz 仓库并找出如何为 nanochat 训练获取更多 token 吗？
