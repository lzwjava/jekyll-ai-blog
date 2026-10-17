---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 使用GitHub OAuth重置仓库
translated: true
type: note
---

两个仓库都已 commit 并 push。每个 remote 都有来自另一台机器的新 commit，所以我在其之上 rebase，而不是 force-push。

## `live-mobile-web` → 已推送 `0c72414..e7225fd`

| Commit | 内容 |
|---|---|
| `ea7176d` feat: 将应用列居中并优化头像/用户列表布局 | 你现有的 WIP（`App.vue`, `Tabbar.vue`, `variables.styl`, `IntroView.vue`, `UsersView.vue`, `user-avatar.vue`） |
| `e7225fd` feat: 添加 GitHub 登录 | `src/common/github.js`, `src/views/GithubCallbackView.vue`, router, `LoginOptionsForm`, `WeiboForm`, `.env.production`, README |

- 已顺利 rebase 到 remote `0c72414`（趣直播图标资源——无文件重叠）。

## `live-server` → 已推送 `9564196..d282dbc`

| Commit | 内容 |
|---|---|
| `d282dbc` feat: 将 GitHub OAuth code 返回给调用方的 SPA | `app/Controllers/Github.php`, `app/Config/Constants.php`, `.env.example` |

- Rebase 在 `app/Config/Constants.php` 中遇到一个冲突：你远程的 GCS 迁移在同一个位置重写了 `QINIU_FILE_HOST*` 的值（现在为 `storage.googleapis.com/qulive`），而我添加了 `GITHUB_LOGIN_REDIRECT_ORIGINS`。解决方案保留了**两者**——远程的 GCS hosts 以及重定向 allow-list——并在继续之前通过了 `php -l` 检查。
- `Github.php` 自动合并；rebase 后验证重定向/allow-list 逻辑完整（`.env.example` 也自动合并）。

两个仓库的工作区都是干净的，远程的其他新提交（GCS 图像存储、`api.funlive.io` nginx vhost、DB URL rewriter）都保留在我的提交之下，未被改动。

部署提醒：push 已完成，但 **live-server 必须先于这个前端构建部署**，否则点击 GitHub 登录会进入旧的 JSON 回调页面。