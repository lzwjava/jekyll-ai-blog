---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Fabfile 部署摘要
translated: true
type: note
---

完成！以下是已创建和部署的内容摘要：

### 项目根目录下的 `fabfile.py`

**用法：**

```bash
# Deploy to remote (rsync + pip install)
fab -H root@36.150.116.206:31005 deploy

# Check deployed version and status
fab -H root@36.150.116.206:31005 status

# Run any command on remote
fab -H root@36.150.116.206:31005 shell -- cmd="ls -la /root/ahl"
```

**功能：**

- **`deploy`** — 使用 rsync 将本地源代码树同步到远程的 `/root/ahl` 目录，排除 `__pycache__`、`.git`、`*.png` 等，然后使用 `/opt/venv/bin/pip`（远程的虚拟环境）运行 `pip install -e .`。
- **`install`** — `deploy` 的别名。
- **`status`** — 显示已部署的版本、pip 包信息和远程文件列表。
- **`shell`** — 通过 SSH 在远程上运行任意命令。