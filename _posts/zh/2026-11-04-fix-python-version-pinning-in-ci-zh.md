---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 修复 CI 中的 Python 版本固定
translated: true
type: note
---

修复了。以下是对 `.github/workflows/gh-pages.yml` 中所做更改的摘要：什么出了问题以及我更改了什么。

**根因：** `ubuntu-latest` 现在运行 Ubuntu 26.04，其托管工具缓存不再包含 CPython `3.13.2`。`setup-python` 失败并报出：
```
##[error]The version '3.13.2' with architecture 'x64' was not found for Ubuntu 26.04.
```

**更改：**
1. **Python 版本** — 将 `python-version: "3.13.2"` 改为 `"3.13"`（不带补丁号）。`setup-python` 现在会解析为 runner 操作系统上最新的可用 3.13.x 版本，而不是固定到一个已被移除的确切补丁版本。
2. **失败通知** — 同时还出现了错误（`No module named 'dotenv'`），因为它直接在没有仓库依赖的情况下运行了裸系统的 `python3`。重写了通过 `curl` 发送到 Telegram 的通知，使得即使在更早的 Python 设置/安装失败时，警报也能可靠触发。

YAML 验证成功。我尚未提交——如果你希望推送，请告知。

**注意：** 在其他 workflow 中也存在相同的 `"3.13.2"` 固定版本，这将会遇到相同的 Ubuntu 26.04 失败：
- `test.yml`、`punch.yml`、`reminders.yml`、`notes.yml`、`news.yml`、`notes-translation.yml`、`nytimes.yml`（全部固定了 `3.13.2`；`translate.yml`/`habit.yml` 已经使用了 `3.x`/`3.13`，所以它们没问题）

要我对其余文件也应用相同的修复吗？