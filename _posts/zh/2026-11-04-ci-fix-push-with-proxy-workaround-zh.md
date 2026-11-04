---
audio: false
generated: true
image: false
lang: zh
layout: post
title: 通过代理变通方案的CI修复推送
translated: true
type: note
---

已推送。GitHub `main` 现在处于 `5ca3c4aa9`，包含了 CI fix。

**发生了什么：**

1. **提交了** `5ca3c4aa9 fix(ci): use patch-less python version for ubuntu-latest`（8 个工作流程文件，所有 hooks 通过）。
2. **推送**遇到了麻烦：
   - `git push origin`（通过 `git@github.com` 的 SSH）现在失败了——你的本地 SOCKS 代理（`localhost:7891`）间歇性地在端口 22 SSH 上进行 MITM 攻击（不寻常的 banner `SSH-2.0-5ec5cb2f`，密钥被拒绝），尽管几分钟前还能工作。
   - 通过代理的 HTTPS 推送最初失败，出现 GitHub `Internal Server Error`——这是通过代理的 HTTP/2 问题。强制使用 **HTTP/1.1** 解决了问题：

     ```
     git -c http.version=HTTP/1.1 push https://github.com/lzwjava/jekyll-ai-blog.git main
     ```

3. **验证**：`git ls-remote ... refs/heads/main` → `5ca3c4aa9`。

两点说明：

- 如果你希望未来的推送更可靠，可以考虑运行 `git config --global http.version HTTP/1.1`（有助于 HTTPS 路径）和/或将 `origin` 改为 HTTPS URL（`git remote set-url origin https://github.com/lzwjava/jekyll-ai-blog.git`），因为你的 `gh` token 适用于此。如果你同意，我可以执行其中任何一项。
- 现在有一些未提交的更改（`_includes/sort.html`、`_sass/layout.scss`），它们是在我执行 `git add -A` 之后出现的——我没有处理它们。要我提交/推送这些更改吗？
