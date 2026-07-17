---
audio: false
generated: true
image: false
lang: zh
layout: post
title: SSH配置清理：从id_rsa到id_ed25519
translated: true
type: note
---

最新的配置已经正确、验证并生效——`runpod`/`runpod-gpu-*`/`runner` 都通过 `id_ed25519` 解析，并且绕过代理。剩下的一处清理是，将 `Host *` 默认块中的 `id_rsa` 移除，以免它被优先尝试。

**~/ssh/config 第 18–24 行：**
```
Host *
    UseKeychain yes
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_rsa     ← 改为 ~/.ssh/id_ed25519
    LogLevel VERBOSE
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

修改后，用法：
- `ssh runner` → `root@213.173.99.50 -p 26246 -i ~/.ssh/id_ed25519`
- `ssh runpod` → `n4pqpw4h5fe3bb-64411f2b@ssh.runpod.io -i ~/.ssh/id_ed25519`
- `ssh runpod-gpu-<podId>` → 相同的 RunPod 用户，内嵌任意租用 IP

用时总结：`runner` 4.8 秒（直连）对比 5.4 秒（通过 DMIT 代理）。`runpod` 仅直连。功能上更清洁——不再需要每次手动匹配主机+用户+端口。