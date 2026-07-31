---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 冒烟测试现在通过了
translated: true
type: note
---

完成——您的冒烟测试现在**通过了**。以下是完整说明：

## 发生了什么

| 运行次数 | 结果 | 原因 |
|---|---|---|
| 第1次 (`00-08-32`) | ✗ 测试超时 @60s | 测试脚本从互联网下载 apt + uv + pytest；您的网络直连速度约 70 kB/s |
| 第2次 (`00-14-54`) | ✗ 超时 @600s | 即使10分钟也不够——仅35 MB的`uv`二进制文件就需要约10分钟 |
| 第3次 (`00-35-42`) | **✅ 100%准确率** | 代理修复——测试在**31.3秒**内完成 |

测试框架本身从未出问题——纯粹是网络速度问题：任务容器没有互联网代理，而您的主机在`127.0.0.1:7890`上运行mihomo（通过它访问GitHub速度达5.4 MB/s）。

## 我修复的内容（3处修改）

1. **`/etc/docker/daemon.json`** — 代理已配置但指向`localhost:7890`（对容器内无效）且从未加载。现在改为：`http://172.17.0.1:7890`（也有助于镜像拉取）。备份已保存为`daemon.json.bak`。
2. **ufw规则** — 您现有规则仅允许端口7890访问`docker0`，但每个基准测试都会创建一个*新的* compose桥接网络。新增：`ufw allow from 172.16.0.0/12 to any port 7890 proto tcp`。
3. **`original-tasks/`下所有241个`docker-compose.yaml`文件** — 注入代理环境变量 + `host.docker.internal:host-gateway`（可通过`T_BENCH_HTTP_PROXY`覆盖）。这才能真正将代理*注入*容器。

## 现在运行您的真实基准测试

```bash
cd /mnt/data/terminal-bench

# 使用DeepSeek运行单个任务
tb run --dataset-path original-tasks --agent terminus \
  --model deepseek/deepseek-chat -t "3d-model-format-legacy" \
  --n-concurrent 1 --no-rebuild

# 完整241任务运行（实际基准测试）
tb run --dataset-path original-tasks --agent terminus \
  --model deepseek/deepseek-chat --n-concurrent 4
```

## 备注

- `git status`显示241个修改的compose文件——随时用`git checkout -- original-tasks`还原（但之后需重新运行补丁：`python3 /tmp/patch_proxy2.py`）。如果您愿意，我可以将该脚本添加到仓库。
- 您的Docker服务全部正常重启。**nextcloud-app-1存在预先存在的问题**（镜像33.0.0.16与数据版本33.0.2.2不匹配——需要通过`docker compose pull`拉取新镜像；快速代理现在让这个操作变得迅速）。
- 完整基准测试提示：首次运行每个任务后使用`--no-rebuild`，注意磁盘空间（每次测试构建约1.5 GB镜像，默认会清理），考虑使用`--n-concurrent 4`以提高吞吐量。

需要我启动一个任务的DeepSeek运行来验证LLM路径吗？