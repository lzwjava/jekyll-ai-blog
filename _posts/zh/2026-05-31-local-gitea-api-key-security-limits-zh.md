---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 本地 Gitea API 密钥安全限制
translated: true
type: note
---

**问题：** 将API密钥存储在本地工作站上自托管的Gitea私有仓库中是否安全？

**回答：**

比GitHub安全得多，但仍然不是存储秘密的正确工具。以下是完整分析：

## 为什么本地Gitea比GitHub更好

| 风险 | GitHub 私有仓库 | 本地Gitea |
|---|---|---|
| GitHub员工访问 | ✅ 存在 | ❌ 消除 |
| GitHub被入侵 | ✅ 真实风险 | ❌ 消除 |
| 意外公开暴露 | ✅ 一键操作 | ❌ 困难得多 |
| 第三方Actions泄露 | ✅ 真实 | ❌ 你控制CI |
| 暴露于互联网的攻击面 | ✅ 总是 | ❌ 仅局域网（配置正确时） |

因此，如果你的Gitea：

- 仅局域网（无端口转发，不暴露于公共域名）
- 只有你能访问
- 运行在你的 `192.168.1.36` 工作站上

……那么实际上风险非常低。对于单人开发者的个人工具来说，这可以说是可以接受的。

---

## 但这些风险依然存在

### 1. Git历史记录仍然是永久性的

和GitHub一样的问题——如果你曾经运行过 `git log`，密钥将永远留在那里。轮换变得痛苦。

```bash
# 密钥已从文件中删除，但仍可见：
git log -p | grep "sk-ant-"
```

### 2. Gitea本身存在漏洞

Gitea曾有过CVE。如果你的工作站位于共享网络（办公室、大学等），网络攻击者可能利用Gitea。

### 3. 备份泄露

如果你备份工作站（Time Machine, rsync, 云备份），你的Gitea数据——包括所有git历史记录——也会被备份。现在你的密钥会出现在备份所在的地方。

### 4. 仓库在多台机器上克隆

你说你有MacBook Air + 工作站 + AMD云服务器。如果你将仓库克隆到三台机器上，密钥将存在于三台机器上，并在通过SSH/HTTPS传输时暴露。

### 5. 随着时间推移，纪律松懈

今天只有你一个人。明天你添加了一个协作者，或者为了方便不小心将Gitea暴露到互联网上。密钥已经存在于历史记录中。

---

## 真正的问题：Git不是存储秘密的正确工具

Git的设计初衷是永不遗忘。秘密需要轮换、过期和撤销。这些目标从根本上是不兼容的。

---

## 针对你的实际推荐方案

考虑到你的三台机器（MacBook + 工作站 + AMD云服务器）：

### 选项1: `pass` — Unix密码管理器（最适合单人开发者）

```bash
# 安装
brew install pass        # macOS
sudo apt install pass    # Ubuntu

# 使用你的GPG密钥初始化
pass init "your@email.com"

# 存储密钥
pass insert llm/anthropic
pass insert llm/openai
pass insert llm/openrouter

# 在脚本中检索
export ANTHROPIC_API_KEY=$(pass llm/anthropic)
```

`pass`将GPG加密的文件存储在 `~/.password-store/` 中——这本身就是一个git仓库，但值是加密存储的。你可以通过Gitea同步它，并且它是安全的，因为秘密在git中是以密文形式存在的。

```bash
# 通过你的本地Gitea在机器之间同步
cd ~/.password-store
git remote add origin http://192.168.1.36:3000/lzw/pass-store.git
git push
```

现在密钥在Gitea中，但是加密的。即使有人克隆了仓库，他们也需要你的GPG私钥。

### 选项2: `direnv` + `.env`（按项目，简单）

```bash
brew install direnv      # macOS
sudo apt install direnv  # Ubuntu

# .envrc（已添加到.gitignore）
export ANTHROPIC_API_KEY="sk-ant-..."
```

```bash
# .gitignore
.envrc
.env
```

`direnv` 会在你 `cd` 进入项目时自动加载环境变量。没有秘密会触及git。

### 选项3: 自托管Infisical（如果你想要一个合适的秘密管理器）

既然你已经本地运行Gitea，你也可以自托管 [Infisical](https://github.com/Infisical/infisical) —— 这是一个开源秘密管理器，带有CLI：

```bash
# 将秘密获取到你的shell中
infisical run -- python my_script.py
```

对于单人使用来说过于复杂，但如果你想扩展到团队，值得了解。

---

## 针对你的个人推荐

```
pass (GPG加密) + 通过本地Gitea同步
```

- 加密存储 → 在git历史记录中安全
- 通过你现有的Gitea在三台机器之间同步
- 原生命令行，可脚本化，无需GUI
- 与你的Python/bash工作流完美配合：

```python
import subprocess
key = subprocess.check_output(["pass", "llm/anthropic"]).decode().strip()
```

或者直接在 `~/.zshrc` 中加载：

```bash
export ANTHROPIC_API_KEY=$(pass llm/anthropic)
export OPENAI_API_KEY=$(pass llm/openai)
export OPENROUTER_API_KEY=$(pass llm/openrouter)
```

---

## 总结

| 方法 | 安全？ | 跨机器同步 | 备注 |
|---|---|---|---|
| 本地Gitea，明文 | ⚠️ 风险低，但工具不对 | ✅ | 历史记录泄露，备份风险 |
| 本地Gitea + `pass` (GPG) | ✅ 良好 | ✅ | 两全其美 |
| `.env` + `direnv`，不使用git | ✅ 良好 | 手动复制 | 简单，无同步 |
| 自托管Infisical | ✅ 最佳 | ✅ | 对单人开发者来说过于复杂 |
| `~/.zshrc` 环境变量 | ✅ 可以 | 手动复制 | 最简单，无同步 |
