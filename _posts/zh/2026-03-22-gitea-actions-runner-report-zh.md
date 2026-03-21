---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Gitea Actions 运行器设置报告
translated: true
type: note
---

老板，这是完整的设置报告。

---

## Gitea Actions Runner — 设置报告

### Binary
- **软件：** `act_runner` v0.2.6（官方 Gitea Actions runner）
- **位置：** `/usr/local/bin/act_runner`

### Registration
- **实例：** `http://192.168.1.36:3000`
- **名称：** `local-runner`
- **UUID：** `68cf95f8-2e71-4610-87f2-6b7ad65f8273`
- **Runner ID：** 1（`lzwjava/blog-source` 的 repo-level runner）
- **状态：** 已成功注册，正在监听任务

### Labels（此 runner 可以拾取的任务类型）

| Label | Runtime |
|---|---|
| `ubuntu-latest` | Docker: `node:16-bullseye` |
| `ubuntu-22.04` | Docker: `node:16-bullseye` |
| `ubuntu-20.04` | Docker: `node:16-bullseye` |
| `ubuntu-18.04` | Docker: `node:16-buster` |

### Runtime Dependencies
- **Docker：** v27.5.1 ✅
- **Systemd：** 已启用（`gitea-runner.service`） ✅
- **重启后存活：** 是

### Configuration
- **配置文件：** `/home/lzw/.gitea-runner/config.yaml`（默认）
- **并发：** 一次 1 个任务
- **任务超时：** 3 小时
- **缓存服务器：** 已启用（自动检测端口）
- **容器网络：** 自动创建
- **获取间隔：** 每 2 秒轮询新任务

### File Locations

| File | Path |
|---|---|
| Config | `/home/lzw/.gitea-runner/config.yaml` |
| Registration | `/home/lzw/.gitea-runner/.runner` |
| Service unit | `/etc/systemd/system/gitea-runner.service` |

### Useful Commands
```bash
# Check status
sudo systemctl status gitea-runner

# Live logs
journalctl -u gitea-runner -f

# Restart after config change
sudo systemctl restart gitea-runner
```

### Things to Note
- 这是 **repo-level runner**（仅限于 `lzwjava/blog-source`），不是 org-wide
- 任务在从 `node:16-bullseye` 拉取的 Docker 容器中运行——首次运行时拉取镜像会较慢
- 默认配置中有占位环境变量（`A_TEST_ENV_NAME_1/2`）——如果需要可以清理
- 容量为 1 ——如果需要并行任务，在配置中增加 `runner.capacity`

有什么想调整的吗？