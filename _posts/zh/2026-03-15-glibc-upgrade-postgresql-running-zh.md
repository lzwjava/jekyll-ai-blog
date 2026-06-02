---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 在 PostgreSQL 运行时升级 glibc
translated: true
type: note
---

问题：在升级 glibc 时 PostgreSQL 正在运行，应该回答 "Yes" 还是 "No"？

回答：

## 回答：**Yes** — 但仅在了解会发生什么之后

这个对话来自 Debian/Ubuntu 系统上的 `libc6` (glibc) 升级过程。以下是您需要知道的内容：

### 对话在告诉您什么

- glibc（GNU C Library）是几乎所有程序使用的核心系统库。
- 使用 NSS (Name Service Switch) 的服务——包括 **PostgreSQL** ——需要在升级后重启以加载新库。
- 安装程序**检测到 PostgreSQL 正在运行**，并警告您它无法自动重启它。

---

### 如果您回答 **Yes**

- 升级会立即进行。
- PostgreSQL 将**继续运行**，但使用旧的内存中 glibc。
- 之后您**必须手动重启 PostgreSQL**：
  ```bash
  sudo systemctl restart postgresql
  ```
- 如果您可以立即重启 PostgreSQL，这在大多数情况下是**推荐的选择**。

---

### 如果您回答 **No**

- 升级将被**暂停/中止**。
- 您可以先手动停止 PostgreSQL：
  ```bash
  sudo systemctl stop postgresql
  ```
- 然后重新运行升级：
  ```bash
  sudo apt-get upgrade
  ```
- 如果您需要**受控维护窗口**或无法承受升级期间 PostgreSQL 不稳定的任何风险，请选择此选项。

---

### 推荐

| 场景 | 回答 |
|---|---|
| 开发/测试服务器，可以重启 PostgreSQL | **Yes** |
| 生产服务器，需要零风险 | **No** （先停止 PostgreSQL，然后重新运行） |
| 正在运行活动连接/事务 | **No** |
| 没有活动数据库连接 | **Yes** |

> ⚠️ 回答 **Yes** 后，升级完成后始终记得立即运行 `sudo systemctl restart postgresql`。
