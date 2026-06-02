---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 将 Homebrew Claude Code 切换到 npm
translated: true
type: note
---

**问题：** 如何移除通过 Homebrew 安装的 Claude Code 并切换到 npm 安装的版本？

**回答：**

## 移除 Homebrew 安装的 Claude Code 并切换到 npm 版本

### 步骤 1：通过 Homebrew 卸载 Claude Code

```bash
brew uninstall claude
```

如果它是作为 cask 安装的：
```bash
brew uninstall --cask claude
```

---

### 步骤 2：验证它已被移除

```bash
which claude
```

它应该返回 **nothing**（或 `claude not found`）。如果仍然显示 `/opt/homebrew/bin/claude`，则强制移除二进制文件：

```bash
rm /opt/homebrew/bin/claude
```

---

### 步骤 3：通过 npm 安装 Claude Code（特定版本）

```bash
npm install -g @anthropic-ai/claude-code@2.1.77
```

---

### 步骤 4：验证 npm 版本已激活

```bash
which claude
claude --version
```

现在你应该看到类似：
```
/Users/yourname/.npm-global/bin/claude   # 或 ~/.nvm/versions/node/.../bin/claude
2.1.77 (Claude Code)
```

---

### 故障排除：PATH 优先级

如果通过 npm 安装后 `which claude` 仍然指向 Homebrew，则你的 `PATH` 将 `/opt/homebrew/bin` 优先于 npm 的 bin 目录。

检查你的 `~/.zshrc` 或 `~/.bash_profile`，确保 npm 的 bin 路径在 **Homebrew 之前**：

```bash
# 在 ~/.zshrc 中 — npm global 在 homebrew 之前
export PATH="$HOME/.npm-global/bin:$PATH"
# 或如果使用 nvm：
export PATH="$HOME/.nvm/versions/node/$(node -v)/bin:$PATH"
```

然后重新加载：
```bash
source ~/.zshrc
```

---

### 快速总结

| 步骤 | 命令 |
|---|---|
| 移除 Homebrew 版本 | `brew uninstall claude` |
| 安装 npm 版本 | `npm install -g @anthropic-ai/claude-code@2.1.77` |
| 验证 | `which claude && claude --version` |
