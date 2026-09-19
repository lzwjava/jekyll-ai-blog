---
audio: false
generated: true
image: false
lang: zh
layout: post
title: Pi端到端验证成功
translated: true
type: note
---

已完成端到端验证。

## `lzw@192.168.1.49` 上的结果

**最终检查：`pi -p "Reply with exactly: PI-WORKS"` → `PI-WORKS`**（通过 `deepseek/deepseek-v4-flash`）。

### 我发现的情况

你**已经自行在 `~/.local` 下安装了 pi**（创建时间 17:52，在我工作期间）——这就是我注意到的 `# Pi` PATH 行和空的 `sessions/` 目录。我当时同时安装了另一份副本到 `~/.npm-global`。两者都是 `0.85.1` 版本，因此我**合并到了你的版本上**：删除了我的 `~/.npm-global` 副本，并撤销了我设置的 npm 前缀（删除 `~/.npmrc` → 恢复为 `/usr/local`）。

### 配置已复制到 `~/.pi/agent/`

| 文件 | 说明 |
| --- | --- |
| `settings.json` | `deepseek` / `deepseek-v4-flash`，thinking=high |
| `models-store.json` | 304 KB 目录（deepseek, mistral, openrouter） |
| `auth.json` | `{}` — 源端同样为空 |
| `trust.json` | `/home/lzw/projects` |
| `AGENTS.md` | 你的全局纯英文规则 |
| `extensions/` | `done-sound.ts`, `note/index.ts`（均使用 `homedir()`，可移植） |
| `bin/fd` | pi 的文件搜索二进制文件 |

**未复制：** `sessions/`（25 MB 的历史记录——这是历史数据，不是配置）。如果需要，请告诉我。

### 环境变量键

已追加到 `~/.bashrc`（12 行，幂等操作）：`DEEPSEEK_API_KEY`, `OPENROUTER_API_KEY`, `MISTRAL_API_KEY`, `CLOUDFLARE_API_KEY`, `CLOUDFLARE_API_TOKEN`, `TELEGRAM_BOT_API_KEY`, `TELEGRAM_LOCATION_BOT_API_KEY`, `SERVER_IP`, `MODEL_PROVIDER`, `MODEL`。跳过了注释掉的 Cloudflare 密钥和特定机器的 `CLASH_EXECUTABLE`（指向目标机上不存在的本地路径）。

还添加了 `~/.local/bin/rg`（ripgrep 14.1.0）——目标机原先没有 `rg` 或 `fd`。

### 三件值得了解的事

1. **一个错误的测试差点让我钻进死胡同。** 我最初的检查使用了 `ssh host 'bash -lc ...'`，pi 报告了 *"No API key found"* 和 *"No models available."* 原因是 Ubuntu 的 `.bashrc` 对非交互式 shell 有提前返回机制——**并非配置问题**。

2. **你的密钥仅在交互式 shell 中加载。** 我用 `env -i` 验证：干净的登录 shell 在**源机和目标机上** `DEEPSEEK=` **均为空**。因此目标机现在完全匹配你源机的行为。但任何非交互式操作——`ssh 192.168.1.49 'pi ...'`、cron、systemd——都将无法通过身份验证。如果你希望将这些密钥移至 `~/.profile` 或 `BASH_ENV` 文件以覆盖这种情况，请告诉我。

3. **`npm install -g` 在目标机上需要 sudo**（前缀已恢复为 `/usr/local`）。你惯用的做法是 `npm install -g --prefix ~/.local`，这也是你安装 pi 的方式。我可以将 `prefix=~/.local` 写入 `~/.npmrc`，使普通的 `npm install -g` 无需 sudo 即可工作——我故意保留了原样，因为这是你机器的默认设置。

上一任务中仍待处理的事项：**mihomo 正在运行（pid 7445），但不是作为服务运行的**，因此它和 pi 的设置将在重启后失效。需要我添加一个 mihomo 的 systemd 用户服务吗？
