---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 并发提交，全部推送
translated: true
type: note
---

全部推送完毕。GitHub 的 `main` 分支现在位于 `f5e6401b3`，工作树是干净的。

推送的内容（按顺序）：
1. `5ca3c4aa9` — `fix(ci)`: 无补丁的 Python 版本（之前的任务）
2. `045c8466f` — `fix(build)`: 移除重复的 posts/marp 冲突 *(非我所为——同时出现在历史中)*
3. `62d9ef190` — `fix(style)`: 暗色模式下 DeepWiki pill 特异性修复
4. `f5e6401b3` — `feat(home)`: 将 notes 设为首页 *(非我所为——一个并发进程将其提交到了我的提交之上)*

提一下最后两条：**另一个进程（或第二个会话）正在积极地提交到这个仓库** — `045c8466f` 和 `f5e6401b3` 不是我提交的，我在 "push all" 时把它们一起推送了。如果那个并发的工作还不应该被上传，请告诉我，我可以帮你整理一下。另外，仍然在使用 HTTPS + `HTTP/1.1` 的变通方案进行推送，因为通过你的代理使用 SSH 会不断被 MITM 攻击 — 考虑运行 `git config --global http.version HTTP/1.1` 来使其永久生效（我可以为你应用这个配置）。