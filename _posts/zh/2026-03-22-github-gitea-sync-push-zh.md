---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 同时推送到 GitHub 和 Gitea
translated: true
type: note
---

**问题：** 如何同时将 Git 仓库推送到 GitHub 和局域网上的本地 Gitea 服务器，以及背后的同步机制是什么？

---

**回答：**

## 同步机制概述

Git 设计为去中心化的。当你的项目同时存在于 Gitea 的 repo 和 GitHub 的 repo 中时，就如同项目存在于两个独立的服务器上——这没有任何矛盾。你可以修改本地副本，提交更改，然后推送到 Gitea、GitHub 或两者同时推送。

默认情况下，GitHub 和 Gitea 之间**没有自动双向同步**。同步是**基于 push 且从本地机器单向的**——你是真相来源，当你 push 时，两个 remote 都会接收你的 commits。Git 的内部机制（pack objects、delta compression）对两个 remote 完全相同；它只是将相同的 commit objects 发送到两个不同的端点。

---

## 方法 1：两个独立的命名 Remote（最灵活）

这是最干净的方法——显式且易于管理。

```bash
# Add GitHub as remote named "github"
git remote add github git@github.com:username/repo.git

# Add local Gitea as remote named "gitea"
git remote add gitea http://192.168.1.x:3000/username/repo.git
# or via SSH: git@192.168.1.x:username/repo.git
```

Git 允许你拥有多个 remote，每个都有自己的名称。将 GitHub 和 Gitea 添加为独立的 remote 意味着你可以同时推送到两者。`git push github main` 将本地 main 的 commits 发送到 GitHub remote，Gitea 同理。

手动推送到两者：

```bash
git push github main
git push gitea main
```

或者创建一个 **Git alias**，用一个命令推送两者：

```bash
git config --global alias.pushall '!git push github main && git push gitea main'
# Then just run:
git pushall
```

---

## 方法 2：单个 Remote 带有多个 Push URL（一个 `git push` 命令）

你可以定义一个指向多个 push URL 的 git remote。例如，创建一个名为 `all` 的 remote，添加第一个 URL，然后添加第二个 URL：

```bash
# Create "all" remote pointing to GitHub
git remote add all git@github.com:username/repo.git

# Add GitHub as 1st push URL
git remote set-url --add --push all git@github.com:username/repo.git

# Add Gitea as 2nd push URL
git remote set-url --add --push all http://192.168.1.x:3000/username/repo.git
```

使用以下命令验证：

```bash
git remote -v
# Output:
# all  git@github.com:username/repo.git (fetch)
# all  git@github.com:username/repo.git (push)
# all  http://192.168.1.x:3000/username/repo.git (push)
```

`git fetch` 或 `git pull` 将使用列表中的第一个 URL，而 `git push` 将推送到该 remote 配置的所有 push URL。

现在一个命令即可推送到两者：

```bash
git push all main
```

---

## 方法 3：修改 `origin` 以推送到两者（如果 `origin` 已存在）

如果你已经有指向 GitHub 的 `origin`：

```bash
# Keep existing origin fetch URL (GitHub)
# Add Gitea as an additional push-only URL
git remote set-url --add --push origin http://192.168.1.x:3000/username/repo.git
```

现在 `origin` 仍然会**从 GitHub fetch**，但会**推送到 GitHub 和 Gitea 两者**。

---

## 方法 4：通过 Git Post-Commit Hook 自动化

你可以使用 `post-commit` hook 在每次 commit 后自动推送到两个 remote。导航到 `.git/hooks/`，创建一个名为 `post-commit` 的文件，并添加以下脚本：

```bash
#!/bin/sh
# Push changes to Gitea
git push gitea main
# Push changes to GitHub
git push github main
```

然后使其可执行：

```bash
chmod +x .git/hooks/post-commit
```

---

## 同步机制总结

| 方面 | 细节 |
|---|---|
| **方向** | Local → 两个 remotes（基于 push） |
| **原子性** | Pushes 是顺序的，不是原子的——一个可能成功而另一个失败 |
| **Fetch/Pull** | 仅从**一个** remote fetch（fetch URL，通常是 GitHub） |
| **冲突处理** | 必须在本地解决；两个 remote 理想情况下应保持同步 |
| **LAN vs Internet** | LAN 上的 Gitea 很快；GitHub push 单独通过互联网 |

---

## 认证提示

- **SSH keys** 是两个 remote 的推荐方式，用于无密码操作。将你的公钥添加到 GitHub 和你的 Gitea 实例。
- **HTTPS with token**：对于 GitHub，使用 Personal Access Token (PAT)；对于 Gitea，也使用 PAT 或 basic auth。
- 如果在 LAN 上，SSH 到 Gitea 通常为：`git@192.168.1.x:username/repo.git`（确保 Gitea 主机上的端口 22 已打开）。

---

**参考资料：**

- [Pushing to multiple Git remotes (jeffkreeftmeijer.com)](https://jeffkreeftmeijer.com/git-multiple-remotes/)
- [How to push to multiple git remotes at once (gist.github.com)](https://gist.github.com/rvl/c3f156e117e22a25f242)
- [Git: Push to multiple remotes at once (leighm.cc)](https://leighm.cc/posts/git-push-to-multiple-remotes-at-once/)
- [Push to Multiple Repositories Using Git Hooks (dev.to)](https://dev.to/nguonodave/push-to-multiple-repositories-simultaneously-using-git-hooks-4cmf)
- [Working with multiple Git remotes (jigarius.com)](https://jigarius.com/blog/multiple-git-remote-repositories)
- [Setting Up a Self-Hosted Github Clone with Gitea (charlesreid1.github.io)](https://charlesreid1.github.io/setting-up-a-self-hosted-github-clone-with-gitea.html)