---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 配置仓库分析与发现
translated: true
type: note
---

已复制并验证。

## `~/projects/config` → `192.168.1.49:~/projects/config`

1.1 MB，整体复制（tar + scp），**保留 `.git`**：

```
git status → ## main...origin/main    (clean)
HEAD → e0b4e25 Add pi done-sound extension
remote → git@github.com:lzwjava/config.git
```

内容：`.bashrc`、`.zprofile`、`config.yaml`、`iTerm.json`、`IDEA-settings.zip`、`README.md`、`claude/settings.json`、`hermes/`（配置+插件）、`openclaw/openclaw.json`、`ww/.env` + `.env.win`、`pi/`、`test.md`。你的 `~/projects/start-pi.sh` 未被改动。

### 有趣的发现：`config.yaml` 是你的 mihomo 配置——而且它比当前运行中的版本*更新*

它是我在第一个任务中安装的相同 mihomo 配置，但仓库副本（`Aug 14`）比当前运行中的版本（`Apr 10`）更新，并且**正好在我遇到问题的地方有所不同**：

```diff
   - name: "Proxy"
     type: select
     proxies:
+      - My Hysteria2 2      # repo: working node FIRST
       - My SS 1             # live: dead node FIRST
   ...
+  - DOMAIN-SUFFIX,kimi.com,Proxy
+  - DOMAIN-SUFFIX,trae.ai,Proxy
+  - DOMAIN-SUFFIX,discord.com,Proxy
```

这种重新排序正是解决我报告的无效节点问题的修复方法——使用这个版本，目标永远不会冷启动到无效的 `My SS 1`。它还添加了3条规则。请注意，仓库没有 `Rules/` 目录，但规则提供者类型为 `type: http`，因此 mihomo 会通过 URL 获取它们。

要我把这个 `config.yaml` 应用到目标机器上作为 mihomo 配置（替换我之前复制的旧版本），并同时在本地更新吗？

### 三个注意事项

1. **仓库中的 `pi/` 快照已经过时——不要将其视为可靠来源。** 它的 `lastChangelogVersion: 0.81.1`，没有 `defaultThinkingLevel`，并且两个扩展都与当前运行中的版本不同。我之前复制的当前运行中的 `~/.pi/agent/`（`0.85.1`，thinking=high）是正确的。仓库中的 `pi/agent/settings.json` 会静默地丢弃你的 `defaultThinkingLevel: high`。

2. **机密信息现在在目标机器上**——`ww/.env` 包含 `GITHUB_TOKEN`、`GITHUB_PAT_TOKEN`、`OPENROUTER_API_KEY`、`GOOGLE_MAPS_API_KEY`。对于配置仓库来说是预期的，但值得注意的是它现在是明文存储在那里。

3. **从目标机器无法使用 git 远程仓库。** 其 `~/.ssh/` 只有 `authorized_keys`（入站），没有密钥，因此：`git@github.com: Permission denied (publickey).` 所以这是一个静态快照——在添加部署密钥或切换到 HTTPS 之前，无法在那里执行 `git pull`。
