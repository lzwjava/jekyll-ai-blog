---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 无需更改；移动API密钥
translated: true
type: note
---

**无需修改——`lzw@192.168.1.34` 上的一切已就绪。**

## 检查结果

`~/.bashrc`（第137行，"代理函数"代码块）：

| 函数 | 行号 | 状态 |
|----------|------|--------|
| `start_proxy` | 139 | ✅ 存在 |
| `start_proxy_without_prefix` | 151 | ✅ 存在 |
| `stop_proxy` | 163 | ✅ 存在 |
| `start_git_proxy` | 176 | ✅ 存在 |
| `stop_git_proxy` | 181 | ✅ 存在 |
| `checkproxy` | 186 | ✅ 存在 |

同时在 `~/.profile` 中也有镜像（第33/45/70行），因此登录 shell 也能获取这些函数。

## 详细信息

- 代理通过 `GLOBAL_PROXY='127.0.0.1:7890'`（第137行）进行配置——两个函数均读取此变量。
- `start_proxy` 设置 `http_proxy`/`https_proxy`/`ftp_proxy`/`ALL_PROXY`，并添加 `http://` 前缀。
- `start_git_proxy` 将 `git config --global http.proxy` 和 `https.proxy` 设置为 `$GLOBAL_PROXY`。
- `NO_PROXY`/`no_proxy` 被导出，并排除了本地/私有地址范围。

**温馨提示：** 该机器上的 `~/.bashrc` 文件第131–132行包含明文的 Cloudflare API 密钥（`CLOUDFLARE_API_KEY`、`CLOUDFLARE_API_TOKEN`）。建议将其移至独立的非跟踪文件（例如在 bashrc 中 source 的 `~/.secrets.env`），或使用 `ww sync` 的模式将其排除在 shell 配置之外。